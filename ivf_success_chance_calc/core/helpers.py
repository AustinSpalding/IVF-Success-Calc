import csv
import math
from django.http import QueryDict
from pathlib import Path

INFERTILITY_CAUSES = [
    'tubal_factor',
    'male_factor_infertility',
    'endometriosis',
    'ovulatory_disorder'
    'diminished_ovarian_reserve',
    'uterine_factor',
    'other_reason'
]

STR_TO_BOOL = {
    'TRUE':True,
    'N/A':None,
    'FALSE':False,
}

def parse_csv_formulae() -> dict[tuple[bool, bool | None, bool], dict] :
    out = {}
    with open(f'{Path(__file__).parent.absolute()}/sources/ivf_success_formulas.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            out[(STR_TO_BOOL[row['param_using_own_eggs']],\
                 STR_TO_BOOL[row['param_attempted_ivf_previously']],\
                 STR_TO_BOOL[row['param_is_reason_for_infertility_known']])] = row
    return out

def calculate_success(fields: QueryDict) -> int:
    using_own_eggs = True if fields.get('using_own_eggs') else False
    ivf_prev = (True if fields.get('ivf_prev') else False) if using_own_eggs else None
    reason_known = True if fields.get('reason_known') else False
    formula = parse_csv_formulae()[(using_own_eggs, ivf_prev, reason_known)]

    score = float(formula['formula_intercept'])
    age = int(fields.get('age'))
    score += age * float(formula['formula_age_linear_coefficient'])
    score += (float(formula['formula_age_power_coefficient']) * (age ** float(formula['formula_age_power_factor'])))

    height_in = int(fields.get('height_ft')) * 12 + int(fields.get('height_in'))
    bmi = (int(fields.get('weight')) / (height_in)**2) * 703
    score += bmi * float(formula['formula_bmi_linear_coefficient'])
    score += (float(formula['formula_bmi_power_coefficient']) * (bmi ** float(formula['formula_bmi_power_factor'])))

    if fields.get('unexplained_infertility', False) :
        score += float(formula['formula_unexplained_infertility_true_value'])
    else :
        for cause in INFERTILITY_CAUSES:
            if fields.get(cause, False):
                score += float(formula[f'formula_{cause}_true_value'])

    preg_prev = int(fields.get('preg_prev'))
    if preg_prev == 1:
        score += float(formula['formula_prior_pregnancies_1_value'])
    elif preg_prev > 1:
        score += float(formula['formula_prior_pregnancies_2+_value'])

    live_births_prev = int(fields.get('live_births_prev'))
    if live_births_prev > preg_prev: # user misunderstanding
        live_births_prev = preg_prev
    if live_births_prev == 1:
        score += float(formula['formula_prior_live_births_1_value'])
    elif live_births_prev > 1:
        score += float(formula['formula_prior_live_births_2+_value'])
    chance = math.exp(score.real) / (1 + math.exp(score.real))
    return round(chance*100)
