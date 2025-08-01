from dataclasses import dataclass
@dataclass
class IPRequest:
    ip_addr: str
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    zip: str
    lat: float
    long: float
    timezone: str
    

@classmethod
def from_dict(cls, data: dict):
    return cls(
        ip_addr=data["query"],
        country=data.get("country"),
        countryCode=data.get("countryCode"),
        region = data.get("region"),
        regionName = data.get("regionName"),
        city = data.get("city"),
        zip = data.get("zip"),
        lat = data.get("lat"),
        long = data.get("long"),
        timezone = data.get("timezone")
    )
