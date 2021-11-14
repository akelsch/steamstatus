from steamstatus.model import Flag, Region

EU_FLAG = Flag("European Union", "eu", True)
US_FLAG = Flag("United States", "us", True)
CHINA_FLAG = Flag("China", "cn")
INDIA_FLAG = Flag("India", "in")

REGIONS = {
    "eu": [
        Region("EU North", EU_FLAG),
        Region("EU East", EU_FLAG),
        Region("EU West", EU_FLAG)
    ],
    "us": [
        Region("US Northcentral", US_FLAG),
        Region("US Northeast", US_FLAG),
        Region("US Northwest", US_FLAG),
        Region("US Southeast", US_FLAG),
        Region("US Southwest", US_FLAG)
    ],
    "china": [
        Region("China Guangzhou", CHINA_FLAG),
        Region("China Shanghai", CHINA_FLAG),
        Region("China Tianjin", CHINA_FLAG)
    ],
    "other": [
        Region("Australia", Flag("Australia", "au")),
        Region("Brazil", Flag("Brazil", "br")),
        Region("Chile", Flag("Chile", "cl")),
        Region("Emirates", Flag("Emirates", "ae", True)),
        Region("Hong Kong", Flag("Hong Kong", "hk")),
        Region("India", INDIA_FLAG),
        Region("India East", INDIA_FLAG),
        Region("Japan", Flag("Japan", "jp")),
        Region("Peru", Flag("Peru", "pe")),
        Region("Poland", Flag("Poland", "pl")),
        Region("Singapore", Flag("Singapore", "sg")),
        Region("South Africa", Flag("South Africa", "za")),
        Region("Spain", Flag("Spain", "es"))
    ]
}
