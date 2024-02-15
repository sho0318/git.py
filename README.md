# git.py
PythonでGitの機能の一部を実装したもの。

## フォルダについて
`src`フォルダと同じ階層以下にあるファイルおよびフォルダを管理する。
例は以下の通りである。
```
.
├ src/
├ git/
├ hoge.txt
└ foo/
    └ bar.txt
```
`git/`は後述するコマンドによって生成されるフォルダで、管理を行う際に使用するファイルの保存先である。

## 機能
### 機能一覧

- add
- commit
- branch
- checkout
- log

### コマンド
#### init
```bash
python src/git.py init
```
初期化を行うコマンド。
オブジェクトなどを管理するフォルダである`git/`が生成される。
すでに`git/`が存在している場合でも、一度削除し、生成しなおすことで、初期化する。

#### add
```bash
python src/git.py add hoge.txt
```
変更したファイルをステージングするコマンド。
同階層にファイルがない場合は`python src/git.py foo/bar.txt`のようにすることでステージングすることができる。
一度に2つ以上のファイルをaddすることはできない。

#### commit
```bash
python src/git.py commit "commit message"
```
ステージングした内容をコミットするコマンド。

#### branch
```bash
python src/git.py branch branchName
```
新しくブランチを作るコマンド。
ブランチの参照先は、HEADが参照している（その時点で作業している）コミットオブジェクトになる。
ブランチ名を入れずに実行すると存在するすべてのブランチ名が表示される。

#### checkout
```bash
python src/git.py checkout branchName
```
作業するブランチを変更するコマンド。
このコマンドを実行したタイミングで、管理しているファイルの中身も更新される。

```bash
python src/git.py checkout-hash commit-hash
```
入力したコミットハッシュを持つコミットオブジェクトに作業する場所を変更するコマンド。
`checkout`と同様にこのコマンドを実行したタイミングで、管理しているファイルの中身が更新される。

#### log
```bash
python src/git.py log
```
作業しているコミットオブジェクト以下のコミットオブジェクトをすべて表示するコマンド。
このコマンドを実行することで、各コミットオブジェクトのコミットハッシュを確認することが可能。

```bash
python src/git.py index
```
現在インデックスに登録されているファイルの情報を表示するコマンド。
ファイル名と対応するハッシュを表示する。
