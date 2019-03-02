from dataclasses import dataclass

import pandas as pd


@dataclass
class SearchResult:
    @dataclass
    class Msa:
        cbsa: int
        name: str = None
        population: dict = None

    zip: int
    cbsa: int = None
    msa: Msa = None


class SearchEngine:
    POPULATION_COLUMN_PREFIX = 'POPESTIMATE'

    def __init__(self, zip_to_cbsa_url, cbsa_to_msa_url):
        zip_to_cbsa_raw_df = pd.read_csv(zip_to_cbsa_url, encoding='latin_1')
        cbsa_to_msa_raw_df = pd.read_csv(cbsa_to_msa_url, encoding='latin_1')

        self.zip_to_cbsa_df = zip_to_cbsa_raw_df[['ZIP', 'CBSA']] \
            .dropna() \
            .loc[zip_to_cbsa_raw_df['CBSA'] != 99999] \
            .drop_duplicates(subset=['ZIP']) \
            .set_index('ZIP')

        self.mdiv_to_cbsa_df = cbsa_to_msa_raw_df[['MDIV', 'CBSA']] \
            .dropna() \
            .drop_duplicates(subset=['MDIV']) \
            .set_index('MDIV')

        self.population_columns = [col for col in cbsa_to_msa_raw_df.columns if col.startswith(self.POPULATION_COLUMN_PREFIX)]

        self.cbsa_to_msa_df = cbsa_to_msa_raw_df[['CBSA', 'NAME'] + self.population_columns] \
            .loc[cbsa_to_msa_raw_df['LSAD'] == 'Metropolitan Statistical Area'] \
            .dropna(subset=['CBSA']) \
            .drop_duplicates(subset=['CBSA']) \
            .set_index('CBSA')

    def _find_zip_cbsa(self, zip_code):
        try:
            return self.zip_to_cbsa_df.loc[zip_code]['CBSA']
        except KeyError:
            return None

    def _find_msa_cbsa(self, zip_csba):
        try:
            return self.mdiv_to_cbsa_df.loc[zip_csba]['CBSA']
        except KeyError:
            return None

    def search_by_zip(self, zip_code):
        zip_cbsa = self._find_zip_cbsa(zip_code)

        if not zip_cbsa:
            return SearchResult(zip=zip_code)

        msa_cbsa = self._find_msa_cbsa(zip_cbsa) or zip_cbsa

        try:
            row = self.cbsa_to_msa_df.loc[msa_cbsa]
            return SearchResult(
                zip=zip_code,
                cbsa=int(zip_cbsa),
                msa=SearchResult.Msa(
                    cbsa=int(msa_cbsa),
                    name=row['NAME'],
                    population={
                        col[len(self.POPULATION_COLUMN_PREFIX):]: int(row[col])
                        for col in self.population_columns
                    }
                )
            )
        except KeyError:
            return SearchResult(zip=zip_code, cbsa=int(zip_cbsa))
