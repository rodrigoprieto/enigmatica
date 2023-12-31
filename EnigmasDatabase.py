import pandas as pd

class EnigmasDatabase:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file).set_index("id")

    def get_enigma(self, enigma_id):
        if self.df[self.df.index == enigma_id].empty:
            return None
        return self.df.loc[enigma_id].to_dict()

    def get_random_enigma(self, enigmas_solved_by_user):
        # Create a new DataFrame that does not include enigmas solved by the user.
        new_df = self.df.drop(enigmas_solved_by_user, errors='ignore')
        if new_df.empty:  # If there are no more enigmas to solve, return False
            return False, {}
        else:
            random = new_df.sample(1)
            return random.index.values[0], random.iloc[0].to_dict()
