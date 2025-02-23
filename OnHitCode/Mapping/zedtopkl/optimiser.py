import 
class TrainingOptimiser():

    def __init__(self, input_folder: str):
        self.json = input_folder

    def training_distributor(self, val: float, test: float, train: float) -> None:
        training_files = os.listdir(self.json)

        print(training_files)

input_json_folder = "OnHitCode/Mapping/zedtopkl/json_clips"

optimiser = TrainingOptimiser(input_json_folder)
optimiser.training_distributor(0.7, 0.2, 0.1)
         