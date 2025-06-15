# Image Identification Tool

このツールは、画像がイラスト（illustration）か写真（photograph）かを自動的に判定するPythonプログラムです。エッジ検出と色分布の分析を組み合わせて、画像の特徴を評価します。

## 機能

- 画像のエッジ検出（Canny法）による特徴抽出
- ガウシアンブラーとメディアンブラーを使用した前処理
- 色分布の分析
- 大サイズ画像の自動リサイズ

## 必要条件

- Python 3.6以上
- OpenCV (cv2)
- NumPy

## インストール方法

### 方法1: requirements.txtを使用

```bash
pip install -r requirements.txt
```

### 方法2: 個別にインストール

```bash
pip install opencv-python numpy
```

## 使用方法

コマンドラインから以下のように実行します：

```bash
python identifiesImage.py <画像ファイルのパス>
```

### 例

```bash
python identifiesImage.py sample.jpg
```

### 出力例

```
score: 0.8 -->illust
```

スコアは0から1の間の値で、0.5以上の場合にイラストと判定されます。

## 判定の仕組み

1. エッジ検出
   - 通常のCannyエッジ検出
   - ガウシアンブラー後のCannyエッジ検出
   - メディアンブラー後のCannyエッジ検出

2. 色分布分析
   - 画像内の色の分布を分析
   - 最も頻出する色の割合を計算

3. スコアリング
   - エッジ検出の結果（80%）
   - 色分布の分析結果（20%）
   - これらの組み合わせで最終スコアを算出

## 注意事項

- 入力画像は一般的な画像形式（JPG, PNG等）に対応
- 2000ピクセル以上の画像は自動的にリサイズされます
- 画像の読み込みに失敗した場合はエラーメッセージを表示
