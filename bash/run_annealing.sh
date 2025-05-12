python -m traveling_salesman \
--coordinates_path inputs/example.txt \
--permutation_output_path outputs/permutation_output/permutation.txt \
--image_output_path outputs/image_output/tour.png \
--init nn \
--cooling geometric \
--num_steps 1_000_000