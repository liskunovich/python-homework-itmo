# LaTeX generator

## Run

### .tex generator

```bash
python homework_2/main.py
```

### .pdf generator

```bash
cd homework_2
docker build -t latex_generator_image .
docker run --rm -v "$(pwd)/output":/app/output latex_generator_image
```
