![Steel gold pan close up at the water's edge, the last of the gravel washed to one side and a single gold flake left settled and bright on the bare steel](intro-banner.png)

# analyze-ioc-extractor

![Wooden sluice run along a shallow river, grey gravel washing in stages down its riffles, a steel pan resting in the shallows at the run's end with washed gravel gathered in it and one small gold flake at its rim](banner.png)

<p align="center"><img src="logo.png" alt="Dark steel gold pan from directly above, grey gravel and green brown water swirling in a ring inside it and one small gold flake settled bright at the pan's rim" width="180"></p>

![Inside the booth scene: a lit ferry crosses slowly, the brass punch closes once on a fresh stub, flags stir, and a gull feather settles](scene.svg)
Extracts Indicators of Compromise (IOCs) such as IP addresses, URLs, and email addresses from a text file or standard input, using regular expressions.

## Install
```sh
git clone https://github.com/ShadowGuard-AI/analyze-ioc-extractor
cd analyze-ioc-extractor
pip install -r requirements.txt
```


![Major section divider](sep-heavy.svg)

## Usage
```sh
python3 main.py [INPUT] [-o OUTPUT] [-i IOC_TYPE] [-v] [-q]
```


![Minor section divider](sep-light.svg)

## Parameters
- `INPUT`: input file, or `-` for stdin. Default: stdin.
- `-h`: show help message and exit.
- `-o`, `--output`: output file in CSV format.
- `-i`, `--ioc-type`: type of IOC to extract: `ip`, `url`, `email`, `md5`, `sha1`, `sha256`, `domain`, or `all`. Default: `all`.
- `-v`, `--verbose`: enable verbose output (logging).
- `-q`, `--quiet`: suppress all output except errors.


![Major section divider](sep-heavy.svg)

## Verified behavior
- A sample containing an IP address, a URL, an email address, an MD5 hash, and a domain produced rows for each of those types.
- With `-i ip`, only the IP row was produced.
- With `-o`, the CSV has two columns, `ioc_type` and `ioc_value`.
- Reading from stdin with `-` works.
- A missing input file exits 1.
- Note on the matches: the URL pattern also matches bare domains and bare IP addresses, so a `url` row is a pattern match, not a validated URL.


![Minor section divider](sep-light.svg)

## License
MIT License, see [LICENSE](LICENSE).

> Counter notice: the URL pattern also matches bare domains and bare IP addresses, so a url row is a pattern match, not a validated URL.
> Counter notice: a missing input file exits with code 1.
