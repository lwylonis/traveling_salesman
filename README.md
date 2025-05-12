# Traveling Salesman Problem &mdash; Simulated Annealing Solver

Efficient and lightweight program for finding approximate solutions to the traveling salesman problem. Given a list of 2D coordinates, it produces a near-optimal tour (permutation of node indices) and a plotted PNG of the tour. 

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/lwylonis/traveling_salesman.git
   cd traveling_salesman
   ```
2. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the solver directly as a Python module:

```bash
python -m traveling_salesman \
--coordinates_path inputs/example.txt \
--permutation_output_path outputs/permutation_output/permutation.txt \
--image_output_path outputs/image_output/tour.png \
--init nn \
--cooling geometric \
--num_steps 1_000_000
```

Or use the bash wrapper:

```bash
bash bash/run_annealing.sh
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)