# Heatwave Simulation

## Deployment & Run

### Deployment

Follow the `AgentSociety` `v1.3.7` setup guide:  
https://agentsociety.readthedocs.io/en/v1.3.7/01-quick-start/#

### Run the Simulation

Run normally:

```bash
./run.sh
```

Or run in the background:

```bash
nohup ./run.sh &
```

## Simulation Logic

The main simulation logic is in `heatwave.py`.

## Output

### Avro Output

Raw Avro output is saved in the `avro-output/` directory.  
Use `avro_convert.py` to convert it to CSV format.

### Logs & Metrics

- Logs are written to `nohup.out` by default.  
- Simulation metrics are available from the configured PostgreSQL server.
