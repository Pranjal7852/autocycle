import logging
import time
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from crewai import Task, Crew

class CrewLogger:
    def __init__(
        self,
        log_file: str = "crew_execution.log",
        log_level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5,
        console_output: bool = True
    ):
        """Initialize the logger with file and console handlers."""
        self.logger = logging.getLogger("CrewLogger")
        self.logger.setLevel(log_level)
        self.task_metrics = []
        self.crew_start_time = None

        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        )
        self.logger.addHandler(file_handler)

        # Optional console handler
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            )
            self.logger.addHandler(console_handler)

    def log_event(self, event: str, metadata: Dict[str, Any]) -> None:
        """Log a generic event with metadata."""
        metadata_str = " ".join(f"{k}={v}" for k, v in metadata.items())
        self.logger.info(f"Event[{event}] {metadata_str}")

    def log_task_execution(self, task: Task, duration: float, metrics: Dict[str, Any]) -> None:
        """Log metrics for a single task execution."""
        task_name = task.description[:50].replace('\n', ' ')
        agent_role = task.agent.role if task.agent else "N/A"
        
        # Debug log to check metrics
        self.logger.debug(f"Raw task metrics: {metrics}")
        
        task_metrics = {
            "task": task_name,
            "agent": agent_role,
            "duration_seconds": round(duration, 3),
            "tokens": {
                "prompt": metrics.get("prompt_tokens", 0),
                "completion": metrics.get("completion_tokens", 0),
                "total": metrics.get("total_tokens", 0)
            }
        }
        self.task_metrics.append(task_metrics)
        tokens_str = f"Tokens(prompt={task_metrics['tokens']['prompt']}, completion={task_metrics['tokens']['completion']}, total={task_metrics['tokens']['total']})"
        self.logger.info(f"Task[{task_name}] Agent[{agent_role}] Duration={task_metrics['duration_seconds']}s {tokens_str}")

    def log_crew_execution(self, crew: Crew, total_duration: float, inputs: Dict[str, Any]) -> None:
        """Log metrics for the entire crew execution."""
        crew_name = crew.__class__.__name__
        
        # Debug log to check crew metrics
        self.logger.debug(f"Raw crew metrics: {crew.usage_metrics}")
        
        # Access UsageMetrics attributes directly
        total_tokens = {
            "prompt": getattr(crew.usage_metrics, "prompt_tokens", 0),
            "completion": getattr(crew.usage_metrics, "completion_tokens", 0),
            "total": getattr(crew.usage_metrics, "total_tokens", 0)
        }
        
        # Calculate total tokens from individual tasks if crew metrics are not available
        if total_tokens["total"] == 0 and self.task_metrics:
            total_tokens = {
                "prompt": sum(task["tokens"]["prompt"] for task in self.task_metrics),
                "completion": sum(task["tokens"]["completion"] for task in self.task_metrics),
                "total": sum(task["tokens"]["total"] for task in self.task_metrics)
            }
        
        inputs_str = " ".join(f"{k}={v}" for k, v in inputs.items())
        tokens_str = f"Tokens(prompt={total_tokens['prompt']}, completion={total_tokens['completion']}, total={total_tokens['total']})"
        tasks_str = f"Tasks[{len(self.task_metrics)}]"
        
        # Log detailed task metrics
        for task in self.task_metrics:
            self.logger.info(f"Task Details: {task}")
            
        self.logger.info(f"Crew[{crew_name}] Duration={round(total_duration, 3)}s {tokens_str} {tasks_str} Inputs[{inputs_str}]")
        self.task_metrics = []  # Reset for next run

    async def execute_task_with_metrics(self, task: Task, inputs: Dict[str, Any]) -> Any:
        """Execute a task and log its metrics."""
        start_time = time.perf_counter()
        result = await task.execute_async(inputs=inputs)
        duration = time.perf_counter() - start_time
        
        # Ensure we have metrics, even if empty
        metrics = task.usage_metrics or {}
        self.log_task_execution(task, duration, metrics)
        return result