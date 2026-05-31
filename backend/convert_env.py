env_dict = {}
with open(".env", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            k, v = line.split("=", 1)
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            env_dict[k] = v

with open("env.yaml", "w") as f:
    for k, v in env_dict.items():
        # Escape double quotes inside the value
        v_escaped = v.replace('"', '\\"')
        f.write(f'{k}: "{v_escaped}"\n')
