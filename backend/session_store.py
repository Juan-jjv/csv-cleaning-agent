from dataclasses import dataclass

import pandas as pd


@dataclass
class SessionData:
    dataframe: pd.DataFrame
    filename: str


sessions: dict[str, SessionData] = {}