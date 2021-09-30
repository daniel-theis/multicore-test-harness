import sys


import json


import sklearn

import pandas as pd


import numpy as np

from matplotlib import pyplot as plt


class ExploreTuningResults(object):

    """A simple plotter for visualizing tuning results.
    Attributes:
        results_json_file:
            Path to json file which contains tuning results.
    """

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


    def build_dataframe(self, k):

        """Convert json results into a single pandas dataframe.
            Args:
                k: key/name for the experiment setup in tune*.json.
            Returns:
                df: dataframe extracted from json formatted result
        """


        def _get_enemy_config(mapping):

            enemy_configs = mapping.split("\n")

            enemy_config = list(set(list(filter(None, enemy_configs))))

            assert len(enemy_config) == 1


            enemy_config = enemy_config[0].split('\t')

            enemy_config = [c.split(' ') for c in enemy_config]


            for i, x in enumerate(enemy_config):

                conf, value = x

                if value.isdigit():

                    enemy_config[i][1] = int(value)


            configs, values = list(zip(*enemy_config))

            return (list(configs), list(values))

        def _get_perf_data(perfdic):
            
            perf_configs=[]
            
            perf_values=[]
            
            for key, value in perfdic[0].items():
                
                perf_configs.append(key)
                
                perf_values.append(value)
            
            return perf_configs, perf_values
        
        result = self.results[k]['it']
        
        columns = ["measurements", "temps", "voluntary_switches", "invluntary_switches"]

        configs, _ = _get_enemy_config(next(iter(result.items()))[1]["mapping"])

        if result['0']['perf']:

            perf_dic, _ = _get_perf_data(result['0']['perf'])
        
            fused = {m: list() for m in columns+configs+perf_dic}
        
        else:

            fused = {m: list() for m in columns+configs}

        for r in result:
            
            perfs=result[r]['perf']
                
            num_exp = len(result[r][columns[0]])
            
            configs, values = _get_enemy_config(result[r]["mapping"])

            for c in columns:

                # assert num_exp == len(result[r][c]), print(c)

                fused[c].extend(result[r][c])
                    
            if result[r]['perf']:

                for i in range(len(perfs)):
                
                    for c in perf_dic:
                 
                        fused[c].append(perfs[i][c])
                
            for c, v in zip(configs, values):

                fused[c].extend([v]*num_exp)
     
            
        df = pd.DataFrame(fused)

        return df


    def plot_results(self, m="measurements", style="box"):

        """Plot function.
        Args:
            m: key of results to plot, example "measurements" or "no_outliers_measurements".
            style: which style to use for plotting; implemented includes box and bar.
        """

        for k in self.results:

            measurements = list()

            result = self.results[k]['it']

            print(f"Get results for {len(result)} enemy configurations.")


            for r in result:

                measurements.append(result[r][m])


            measurements_flattened = [m for c in measurements for m in c ]

            min_measurement = min(measurements_flattened)

            max_measurement = max(measurements_flattened)


            print(f"Minimum of victim measurement {min_measurement}\n"

                  f"Maximum of victim measurement {max_measurement}\n"

                  f"Ratio max2min {max_measurement/min_measurement}\n"

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

    data_explorer = ExploreTuningResults(sys.argv[1])

    # data_explorer.plot_results(m="no_outliers_measurements", style="bar")

    data_explorer.build_dataframe("L1_bo_tune_perf")
