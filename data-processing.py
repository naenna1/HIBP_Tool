from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from datetime import datetime
import json
import math

@dataclass
class Breach:
    name: str
    domain: str
    breach_date: date
    added_date: Optional[date]
    data_classes: List[str]
    pwn_count: int
    is_verified: bool
    is_MalWare: bool    # added to calc risk
    is_StealerLog: bool # added to calc risk

@dataclass
class Paste:
    id: str
    source: str
    date: Optional[datetime]
    email_count: Optional[int]

@dataclass
class BreachSummary:
    breaches: List[Breach]
    risk_score: float

def parse_breach_list(json_data: list[dict]) -> List[Breach]:
    breaches = []
    for item in json_data:
        bd = item.get('BreachDate')
        ad = item.get('AddedDate')
        breach_date = datetime.strptime(bd, '%Y-%m-%d').date() if bd else None
        added_date = datetime.strptime(ad, '%Y-%m-%dT%H:%M:%SZ').date() if ad else None

        breach = Breach(
            name = item.get('Name'),
            domain = item.get('Domain'),
            breach_date = breach_date,
            added_date = added_date,
            data_classes = item.get('DataClasses',[]),
            pwn_count = item.get('PwnCount',0),
            is_verified = item.get('IsVerified',False),
            is_MalWare = item.get('IsMalware',False),           # added to calc risk
            is_StealerLog = item.get('IsStealerLog',False)      # added to calc risk
        )
        breaches.append(breach)
    return breaches

def parse_paste_list(json_data: list[dict]) -> List[Paste]:
    pastes = []
    for item in json_data:
        d = item.get('Date')
        paste = Paste(
            id = item.get('Id'),
            source = item.get('Source'),
            date = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ').date() if d else None,
            email_count = item.get('EmailCount'),
        )
        pastes.append(paste)
    return pastes

#breaches grouped by year
def group_breaches_by_year(breaches: List[Breach]) -> dict[int, List[Breach]]:
    result = {}
    for breach in breaches:
        result.setdefault(breach.breach_date.year, []).append(breach)
    return result

# breaches grouped by domain
def group_breaches_by_domain(breaches: List[Breach]) -> dict[str, List[Breach]]:
    result = {}
    for breach in breaches:
        domain = breach.domain
        result.setdefault(domain, []).append(breach)
    return result

# calc risk score:
#   - there is no official calc method
#   - normalization is difficult (0-100-model)
#   - idea: score weight on data_classes, which is the label of leaked information https://haveibeenpwned.com/api/v3/dataclasses
#   - there are 150 entries in dataclasses, typical labels are chosen manually to calc.

def calculate_risk_score(breaches: List[Breach]) -> float:
    with open("data_class_risk_map.json","r",encoding="utf-8") as f:
        risk_factors = json.load(f)

    high = risk_factors['high']
    medium = risk_factors['medium']
    low = risk_factors['low']
    weight = risk_factors['weight']
    event_tag = risk_factors['event_tag']

    risk_score = 0

    for breach in breaches:
        for entry in breach.data_classes:
            if entry in high:
                risk_score += weight['high']
            elif entry in medium:
                risk_score += weight['medium']
            elif entry in low:
                risk_score += weight['low']
            else:
                risk_score += 1

        if breach.is_MalWare:
            risk_score += event_tag['malware']
        if breach.is_StealerLog:
            risk_score += event_tag['stealerLog']
        if breach.is_verified:
            risk_score += event_tag['verified']

        risk_score = int(risk_score + math.log10(breach.pwn_count + 1) * 2)

    return risk_score

# combines breach with its score
def build_breach_summary(breaches: List[Breach]) -> BreachSummary:
    score = calculate_risk_score(breaches)

    return BreachSummary(
        breaches = breaches,
        risk_score = score
    )