from config import settings


class ProxyStorage:
    """In-memory storage for managing the list of proxies."""

    def __init__(self) -> None:
        self.base_domain: str = settings.PROXY_BASE_DOMAIN
        self.proxies: list = [
            f"{self.base_domain}45.137.52.205:63958",
            f"{self.base_domain}45.137.52.168:63312",
            f"{self.base_domain}45.137.52.184:64872",
            f"{self.base_domain}154.81.42.62:63590",
            f"{self.base_domain}45.137.52.212:64968",
            f"{self.base_domain}5.42.192.93:62908",
            f"{self.base_domain}45.137.52.77:64160",
            f"{self.base_domain}5.42.192.107:63056",
            f"{self.base_domain}156.233.204.231:64010",
            f"{self.base_domain}156.233.204.98:64010",
            f"{self.base_domain}156.233.204.59:64010",
            f"{self.base_domain}156.246.164.185:64298",
            f"{self.base_domain}45.195.189.183:64024",
            f"{self.base_domain}45.195.189.142:64024",
            f"{self.base_domain}45.195.189.103:64024",
            f"{self.base_domain}45.195.189.99:64024",
            f"{self.base_domain}45.195.189.97:64024",
            f"{self.base_domain}154.81.41.48:63250",
            f"{self.base_domain}166.1.180.242:64976",
            f"{self.base_domain}172.120.158.194:62726",
            f"{self.base_domain}166.88.76.31:63508",
            f"{self.base_domain}185.68.81.82:63194",
            f"{self.base_domain}31.222.249.32:63092",
            f"{self.base_domain}166.1.116.22:64742",
            f"{self.base_domain}154.94.39.132:63988",
            f"{self.base_domain}146.19.15.110:64378",
            f"{self.base_domain}138.249.221.200:62580",
            f"{self.base_domain}138.249.132.69:61962",
        ]


storage = ProxyStorage()
