from support import *
from algos import BFS,DFS,UCS, ASTAR
import json

# Dictionary to hold results for each input case
dict = {
    "01": [[], [], [], []],
    "02": [[], [], [], []],
    "03": [[], [], [], []],
    "04": [[], [], [], []],
    "05": [[], [], [], []],
    "06": [[], [], [], []],
    "07": [[], [], [], []],
    "08": [[], [], [], []],
    "09": [[], [], [], []],
    "10": [[], [], [], []],
    "11": [[], [], [], []],
    "12": [[], [], [], []]
}

def save_results_to_json(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

# List of input cases
input_numbers = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
folder_path = './input'  # Folder containing input files

def output2(algo, input_path, output_path):
    grid, ares_start, stones, switches, weights = createMatrix(input_path)
    # Thêm trọng số cho vị trí đá
    new_stones = [(stones[i][0], stones[i][1], weights[i]) for i in range(len(stones))]

    # Usage in the main function
    start_time = time.time()
    # Execute your algorithm
    mem_usage, result = memory_usage((algo, (grid, ares_start, new_stones, switches)), retval=True)
    end_time = time.time()

    with open(output_path, 'a') as file:
        if result is not None:
            node, path = result
            total_time = 1000 * (end_time - start_time)  # Thời gian chạy (ms)
            usage = max(mem_usage) - min(mem_usage)      # Dung lượng bộ nhớ đã sử dụng (MB)
            weight = path[-1].cost                       # Trọng số cuối cùng
            steps = ""
            costs = []

            for i in range(1, len(path)):
                if all(stone in path[i - 1].stones for stone in path[i].stones):
                    if path[i].ares_pos[1] < path[i - 1].ares_pos[1]:
                        steps += 'l'
                    elif path[i].ares_pos[1] > path[i - 1].ares_pos[1]:
                        steps += 'r'
                    elif path[i].ares_pos[0] < path[i - 1].ares_pos[0]:
                        steps += 'u'
                    else:
                        steps += 'd'
                else:
                    if path[i].ares_pos[1] < path[i - 1].ares_pos[1]:
                        steps += 'L'
                    elif path[i].ares_pos[1] > path[i - 1].ares_pos[1]:
                        steps += 'R'
                    elif path[i].ares_pos[0] < path[i - 1].ares_pos[0]:
                        steps += 'U'
                    else:
                        steps += 'D'

                costs.append(path[i].cost)
            # Ghi ra tệp
            file.write(f"{algo.__name__}\n")
            file.write(f"Steps: {len(steps)}, Weight: {weight -  len(steps)}, Node: {node}, Time (ms): {total_time:.2f}, Memory (MB): {usage:.2f}\n")
            file.write(steps + "\n")
            # print
            print(f"{algo.__name__}\n")
            print(f"Steps: {len(steps)}, Weight: {weight -  len(steps)}, Node: {node}, Time (ms): {total_time:.2f}, Memory (MB): {usage:.2f}\n")
            print(steps + "\n")
        else:
            print(algo.__name__)
            print("No solution found")
            file.write(f"{algo.__name__}\n")
            file.write("No solution found\n")
            return [], None, None, None

    return costs, steps, total_time, len(steps)


def main():
    # Iterate over each input case
    for input in input_numbers:
        file_name = f"input-{input}.txt"
        file_path = f"{folder_path}/{file_name}"

        # BFS
        costs, steps, timespent, total_step = output2(BFS, input_path=file_path, output_path='./output-restored/output-'+input+'.txt')
        costs = [0] + costs
        dict[input][0] = [steps, timespent, costs, total_step]
        # DFS
        costs, steps, timespent, total_step = output2(DFS, input_path=file_path, output_path='./output-restored/output-'+input+'.txt')
        costs = [0] + costs
        dict[input][1] = [steps, timespent, costs, total_step]
        # UCS
        costs, steps, timespent, total_step = output2(UCS, input_path=file_path, output_path='./output-restored/output-'+input+'.txt')
        costs = [0] + costs
        dict[input][2] = [steps, timespent, costs, total_step]
        # ASTAR
        costs, steps, timespent, total_step = output2(ASTAR, input_path=file_path, output_path='./output-restored/output-'+input+'.txt')
        costs = [0] + costs
        dict[input][3] = [steps, timespent, costs, total_step]
    save_results_to_json('./output-restored/results.json', dict)



if __name__ == "__main__":
    main()  # Run the main function
