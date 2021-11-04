import sys

import json


import numpy as np

from matplotlib import pyplot as plt


class PlotTuningResults(object):


    def __init__(self, results_json_file=None):

        if results_json_file:

            self.load_results(results_json_file)

        else:

            print("Please specify the results json file.")


    def load_results(self, results_json_file):

        self.results_json_file = results_json_file

        with open(results_json_file) as file:

            self.results = json.load(file)

            print(f"Get results for {len(self.results)} tuning configs.")


    def plot_results(self, m="measurements", style="box"):

        for k in self.results:

            measurements = list()

            result = self.results[k]['it']

            print(f"Get results for {len(result)} enemy configurations.")


            for r in result:

                measurements.append(result[r][m])


            measurements_flattened = [m for c in measurements for m in c ]
            
            avg_measurement = np.mean(measurements_flattened)

            min_measurement = min(measurements_flattened)

            max_measurement = max(measurements_flattened)


            print(f"SUT: {self.results[k]['sut']}\n"

                  f"PERF:{self.results[k]['instrument_cmd']}\n"

                  f"Avg of victim measurement {avg_measurement}\n"

                  f"Minimum of victim measurement {min_measurement}\n"

                  f"Maximum of victim measurement {max_measurement}\n"

                  f"Ration max2min {max_measurement/min_measurement}\n"

            )



            means = [np.mean(c) for c in measurements]

            std_devs = [np.std(c) for c in measurements]

            x_pos = np.arange(len(measurements))


            fig, ax = plt.subplots(figsize=(20,10))


            if style not in ["bar", "box"]:

                print("Plot style not supported.")

                return


            if style == "bar":

                ax.bar(x_pos, means, yerr=std_devs, align='center', alpha=0.5, ecolor='black', width=0.3, capsize=2)

                ax.set_ylabel(m)

                ax.set_xticks(np.arange(len(measurements), step=5))

                ax.yaxis.grid(True)


            elif style == "box":

                ax.boxplot(measurements, widths=0.1)


            ax.set_title(f'Tuning results for {k}')

            plt.tight_layout()

            plt.savefig(self.results_json_file.split(".")[0] + "_" + style + ".png")

            plt.show()



if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("usage: " + sys.argv[0] + "result.json\n")

        exit(1)

    plotter = PlotTuningResults(sys.argv[1])

    plotter.plot_results(style="bar")

