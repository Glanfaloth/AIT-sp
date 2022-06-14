# sptdwait

<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Glanfaloth/sptdwait">
  </a>
  <h3 align="center">Synthesis of Egocentric View for Dynamic Object Tracking</h3>
  <a href="http://www.youtube.com/watch?v=z2y0obcq0Tw" target="_blank">
    <img src="http://img.youtube.com/vi/z2y0obcq0Tw/0.jpg" alt="AIT"/>
  </a>
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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

EN: This project utilizes ThreeDWorld to create several virtual scenes with procedurally generated objects. A simple GUI is designed to customize and randomize the scene settings. With an Oculus Quest headset and controllers, users can interact with the objects in a Virtual Reality environment using virtual hands, while the image sequences will be automatically rendered, including RGB, depth and segmentation mask.

<details>
  <summary>DE</summary>
  Dieses Projekt nutzt ThreeDWorld, um diverse virtuelle Szenen mit prozedural generierten Objekten zu erzeugen. Eine einfache GUI wurde erzeugt, um Szeneneinstellungen anzupassen oder zu randomisieren. Mit einem Oculus Quest Headset und Controllern, können Nutzer mit den Objekten in einer VR Szene mit virtuellen Händen interagieren, während Bildsequenzen, in Form von RGB, Tiefe und Segmentierungsmaske, automatisch gerendert werden.
</details>

<details>
  <summary>FR</summary>
  Ce projet utilise ThreeDWorld pour créer plusieurs scènes virtuelles avec des objets générés de manière procédurale. Une GUI simple est conçue pour personnaliser et randomiser les paramètres de la scène. Avec un casque et des contrôleurs Oculus Quest, les utilisateurs peuvent interagir avec les objets dans un environnement de réalité virtuelle en utilisant des mains virtuelles, tandis que les séquences d'images seront automatiquement rendues, y compris le RVB, la carte de disparité et le masque de segmentation.
</details>

<details>
  <summary>IT</summary>
  Questo progetto utilizza ThreeDWorld per creare diverse scene virtuali con oggetti generati proceduralmente. Una semplice GUI è stata disegnata per personalizzare e randomizzare le impostazioni della scena. Attraverso un headset Oculus Quest e i controller, l'utilizzatore può interagire con gli oggetti nell'ambiente nella realtà virtuale usando mani virtuali, mentre la sequenza di immagini viene automaticamente renderizzata, includendo i colori, la profondità e la maschera di segmentazione.
</details>

<details>
  <summary>ZH</summary>
  本项目运用ThreeDWorld创建了带有过程生成物品的若干虚拟场景，设计了用于自定义或随机设置场景的图形用户界面。通过Oculus Quest头戴设备和控制手柄，用户可在虚拟现实场景中用虚拟手与物品交互，同时渲染出一系列场景的RGB图、深度图和分割图。
</details>

<details>
  <summary>JA</summary>
  このプロジェクトは、ThreedWorldを使用して、いくつかの仮想シーンを手続き型生成されたオブジェクトを作成します。シンプルなGUIをカスタマイズし、シーンの設定をランダムに設計されます。Oculus Questヘッドセットとコントローラで、ユーザーは仮想の手を使っているバーチャル・リアリティの環境でオブジェクトと操作することができます。その一方で、イメージシーケンスはRGB、深さとセグメンテーション・マスクを含む自動的に提出されます。
</details>

<details>
  <summary>DE-CH</summary>
  S projekt brucht ThreeDWorld um verschiedeni virtuelli szene mit prozedural generierte objekt z erzüge. E eifachi GUI isch erzügt worde um szeneiistellige azpasse oder z randomisiere. Mit emene Oculus Quest Headset und controller chönd benützer mit de objekt inere VR szene mit virtuelle händ interagiere während bildsequenze in form vo RGB, tüfi und segmentierigsmaske automatisch grendert werdet.
</details>

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* [ThreeDWorld]([https://nextjs.org/](https://github.com/threedworld-mit/tdw))
* [tkinter]([https://reactjs.org/](https://docs.python.org/3/library/tkinter.html))

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Windows10
* [A compatible GPU](https://support.oculus.com/articles/headsets-and-accessories/oculus-link/oculus-link-compatibility/)
* Oculus headset (Rift, Rift S, Quest, or Quest 2)
* *Quest and Quest 2:* An Oculus Link Cable
* [The Oculus PC app](https://www.oculus.com/setup/)
* Python 3.6+
* tdw
  ```sh
  pip3 install tdw --user
  ```

### Usage

1. Clone the repo
   ```sh
   git clone https://github.com/Glanfaloth/sptdwait.git
   ```
2. Connect Oculus Headset to your PC with an Oculus Link Cable
3. Run the Oculus PC app
5. CD to the repo
6. Run `gui.py`
   ```sh
   python3 .\utils\gui.py
   ```
7. Quit the program by pressing the left trigger button. The results will be stored in `tdw_example_controller_output` folder of the home directory.
8. Convert the depth value to depth maps using `loadnpy.py`
  ```sh
  python3 .\utils\loadnpy.py --scene {scene_name} --name {sequence_name}
  ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [ThreeDWorld]([https://nextjs.org/](https://github.com/threedworld-mit/tdw))

<p align="right">(<a href="#top">back to top</a>)</p>
