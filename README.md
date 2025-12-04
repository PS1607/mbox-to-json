[Open in Visual Studio Code](https://github1s.com/PS1607/mbox-to-json)

<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<sup>Prakhar Sharma - </sup>[![LinkedIn][linkedin-shield]][linkedin-url]<br>
<sup>Adrita Bhattacharya - </sup>[![LinkedIn][linkedin-shield]][linkedin-url2]

<h1 align="center">MBOX to JSON</h1>

  <p align="center">
    A command line tool to convert MBOX file to JSON.
    <br />
    <a href="https://github.com/PS1607/mbox-to-json"><strong>Explore the docs » (Currently NA)</strong></a>
    <br />
    <br />
    <a href="https://github.com/PS1607/mbox-to-json/">View Demo</a>
     · 
    <a href="https://github.com/PS1607/mbox-to-json/issues">Report Bug</a>
     · 
    <a href="https://github.com/PS1607/mbox-to-json/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<br>
<!-- ABOUT THE PROJECT -->

## About The Project

A small package that converts MBOX files to JSON. Also includes functionality to extract attachments with complete traceability.

**✨ Key Features:**
- 📧 Convert MBOX to JSON or CSV format
- 📎 Extract attachments with metadata tracking
- 🔗 Cross-reference attachments to source emails  
- 📊 Split large outputs into manageable chunks
- 🛡️ Robust error handling and logging
- ⚡ Modern Python packaging with flexible dependencies

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

There are 2 ways to install this tool.<br><br>

### Prerequisites

Make sure you upgrade `pip` before moving on.<br>
All the required dependencies are in [`requirements.txt`](https://github.com/PS1607/mbox-to-json/blob/main/requirements.txt) which would be installed at the time of running the setup.

```sh
pip install --upgrade pip
```

<br>

### 1. Install from [PyPI](https://pypi.org/project/mbox-to-json/)

```sh
pip install mbox-to-json
```

<br>

### 2. Install from GitHub

1. Download the repository as zip. Unzip.
2. `cd` to the repository folder
3. Run this command

   ```sh
   pip install .
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

- Help Function

  ```sh
  mbox-to-json -h
  ```

- Most basic conversion from MBOX to JSON. Just provide the file path. Output JSON file would be in the same location as the input file.

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox
  ```

- Use **`-a`** flag to extract attachments. The files would be available in **`input_file_directory/attachments`**

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -a
  ```

- Use **`-a --skip-attachment-metadata`** to extract attachments but keep JSON/CSV output clean (without attachment metadata)

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -a --skip-attachment-metadata
  ```

- Use **`-c`** flag to convert to CSV instead of JSON. Output CSV file would be in the same location as the input file.

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -c
  ```

- Use **`-s`** to split large output into multiple files

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -s 3
  ```

- Use **`--max-payload-size`** to set maximum email payload size in MB (default: 10MB)

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox --max-payload-size 50
  ```

- Use **`--max-body-part-size`** to set maximum body part size in MB (default: 1MB)

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox --max-body-part-size 5
  ```

- Use **`--max-recursion-depth`** to set maximum recursion depth for nested emails (default: 50)

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox --max-recursion-depth 100
  ```

- Use **`--workers`** to set number of parallel workers (default: 1, automatically limited by CPU cores)

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox --workers 4
  ```

- Use **`--enable-parallel`** to force parallel processing regardless of file size or message count

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox --workers 4 --enable-parallel
  ```

- Use **`-o`** to specify the output file location. Make sure to provide the file name too, with the extension JSON (or CSV)
  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -o /Users/prakhar/downloads/random_output.json
  ```

_For more examples, please refer to the [Documentation](https://pypi.org/project/mbox-to-json/)_

### Output Files

When using the `-a` flag, mbox-to-json creates several output files for complete attachment tracking:

- **Main output file** (JSON/CSV): Contains email data with attachment metadata (unless `--skip-attachment-metadata` is used)
- **`*_attachments_manifest.json`**: Complete inventory of all attachments with source email references
- **`attachments/`** folder: Contains extracted attachment files
- **Individual `.metadata.json` files**: Detailed metadata for each extracted attachment
- **`extraction_map.json`**: Complete mapping of attachments to source emails

### Memory Optimization for Large Files

For large MBOX files that may cause memory issues or recursion errors, you can adjust processing parameters:

```sh
# For very large files - increase payload limits and reduce batch size
mbox-to-json large_inbox.mbox --max-payload-size 50 --batch-size 500

# For systems with limited memory - reduce limits
mbox-to-json inbox.mbox --max-payload-size 5 --max-body-part-size 0.5 --batch-size 2000

# For deeply nested email threads - increase recursion depth
mbox-to-json complex_threads.mbox --max-recursion-depth 100

# Use parallel processing for faster performance (automatically uses available CPU cores)
mbox-to-json large_inbox.mbox --workers 4 --batch-size 500

# Force parallel processing for smaller files that don't meet automatic thresholds
mbox-to-json medium_inbox.mbox --workers 4 --enable-parallel

# Disable parallel processing entirely (use serial processing)
mbox-to-json any_inbox.mbox --workers 1

# Combine options for optimal performance with parallel processing
mbox-to-json inbox.mbox -a -c --workers 8 --enable-parallel --max-payload-size 20 --batch-size 250 -o output.csv
```

### Performance Tips

- **Intelligent Parallel Processing**: Automatically enabled for files ≥200MB with ≥1000 messages
- **Force Parallel Processing**: Use `--enable-parallel` to override automatic decision for any file size
- **Worker Optimization**: Set `--workers` to match your CPU core count for maximum performance
- **Memory Management**: Adjust `--batch-size` based on available RAM (lower for limited memory)
- **Large Files**: Increase `--max-payload-size` for files with large attachments
- **Processing Mode**: Tool will log why parallel/serial processing was chosen

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] TBA

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE.txt`](https://github.com/PS1607/mbox-to-json/blob/main/LICENSE.txt) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

LinkedIn - [Prakhar Sharma](https://www.linkedin.com/in/prakhar-sharma-2020/), [Adrita Bhattacharya](https://www.linkedin.com/in/adrita-bhattacharya-6bab581a9/)

Github - [PS1607](https://github.com/PS1607), [adritabhattacharya](https://github.com/adritabhattacharya)

Google Developer - [PS1607](https://g.dev/ps1607)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/dyte-submissions/dyte-vit-2022-PS1607.svg?style=for-the-badge
[contributors-url]: https://github.com/PS1607/mbox-to-json/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dyte-submissions/dyte-vit-2022-PS1607.svg?style=for-the-badge
[forks-url]: https://github.com/PS1607/mbox-to-json/network/members
[stars-shield]: https://img.shields.io/github/stars/dyte-submissions/dyte-vit-2022-PS1607.svg?style=for-the-badge
[stars-url]: https://github.com/PS1607/mbox-to-json/stargazers
[issues-shield]: https://img.shields.io/github/issues/dyte-submissions/dyte-vit-2022-PS1607.svg?style=for-the-badge
[issues-url]: https://github.com/PS1607/mbox-to-json/issues
[license-shield]: https://img.shields.io/github/license/dyte-submissions/dyte-vit-2022-PS1607.svg?style=for-the-badge
[license-url]: https://github.com/PS1607/mbox-to-json/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/prakhar-sharma-2020/
[linkedin-url2]: https://www.linkedin.com/in/adrita-bhattacharya-6bab581a9/
