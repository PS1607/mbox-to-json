[![Open in Visual Studio Code](https://camo.githubusercontent.com/5cf0e57d39fcba2c6db6323c5a38febeef0dbf230a1207efa846063cdf9dbeff/68747470733a2f2f636c617373726f6f6d2e6769746875622e636f6d2f6173736574732f6f70656e2d696e2d7673636f64652d633636363438616637656233666538626334663239343534366266643836656634373337383063646531646561343837643363346666333534393433633961652e737667)](https://github1s.com/PS1607/mbox-to-json)

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

A small package that converts MBOX files to JSON. Also includes functionality to extract attachments.

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

- Use **`-c`** flag to convert to CSV insted of JSON. Output CSV file would be in the same location as the input file.

  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -c
  ```

- Use **`-o`** to specify the output file location. Make sure to provide the file name too, with the extension JSON (or CSV)
  ```sh
  mbox-to-json /Users/prakhar/downloads/random_file.mbox -o /Users/prakhar/downloads/random_output.json
  ```

_For more examples, please refer to the [Documentation](https://pypi.org/project/mbox-to-json/)_

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
