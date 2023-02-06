[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://github1s.com/PS1607/mbox-to-json)

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
<details>
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

<!-- ABOUT THE PROJECT -->

## About The Project

A small package that converts MBOX files to JSON. Also includes functionality to extract attachments.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To run this tool on your system locally, follow the installation steps.

### Prerequisites

Make sure you upgrade `pip` before moving on.
All the required dependencies are in [`requirements.txt`](https://github.com/PS1607/mbox-to-json/blob/main/requirements.txt) which would be installed at the time of running the setup.

```sh
pip install --upgrade pip
```

### Installation

1. Download the repository as zip. Unzip.
2. `cd` to the repository folder
3. Run this command

   ```sh
   pip install .
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

```sh
mbox-to-json -h
```

Usage example#1

```sh
mbox-to-json /Users/prakhar/downloads/random_file.mbox
```

<br>---> Use `-a` flag to extract attachments. The files would be available in an _**attachments**_ folder in the root location of the repo.<br>

Usage example#2

```sh
mbox-to-json /Users/prakhar/downloads/random_file.mbox -a
```

<br>---> Use `-o` to specify the output file location. It defaults to `file.json` in the root location of the repo.<br>

Usage example#3

```sh
mbox-to-json /Users/prakhar/downloads/random_file.mbox -o /Users/prakhar/downloads/random_output.json
```

_For more examples, please refer to the [Documentation](https://doesnotexist.com)_

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

Github: [PS1607](https://github.com/PS1607), [adritabhattacharya](https://github.com/adritabhattacharya)

Google Developer: [PS1607](https://g.dev/ps1607)

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
