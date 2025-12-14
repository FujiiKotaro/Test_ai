# Requirements Document

## Project Description (Input)
Numpy配列を読み込んで，データのグラフ化，可視化，様々なデータの分析や，拡大表示などの機能を備えたpythonスクリプト

## Introduction
本仕様書は、Numpy配列を基にしたデータ可視化・分析ツールの要件を定義します。本ツールは、科学データや数値データの探索的分析を支援するPythonスクリプトとして、グラフ化、可視化、統計分析、インタラクティブな拡大表示、周波数解析（FFT）などの機能を提供します。主な対象データは1次元（1列）のNumpy配列ですが、多次元データにも対応します。

## Requirements

### Requirement 1: データ読み込み機能
**Objective:** As a データアナリスト, I want Numpy配列形式のデータを読み込む機能, so that 様々なソースからのデータを統一的に扱える

#### Acceptance Criteria
1. The Visualizerスクリプト shall Numpy配列（.npy、.npzファイル）を読み込む機能を提供する
2. When ユーザーがファイルパスを指定した場合, the Visualizerスクリプト shall 指定されたファイルからNumpy配列を正常に読み込む
3. If ファイルが存在しない、または読み込めない場合, then the Visualizerスクリプト shall エラーメッセージを表示し、処理を継続可能な状態に保つ
4. The Visualizerスクリプト shall 1次元配列を主な対象としてサポートし、2次元、3次元のNumpy配列もサポートする
5. When 複数の配列を含む.npzファイルを読み込んだ場合, the Visualizerスクリプト shall 各配列を識別可能な形で保持する
6. The Visualizerスクリプト shall 1列形式のデータ（1次元配列）を最適に処理する機能を提供する

### Requirement 2: データグラフ化機能
**Objective:** As a データアナリスト, I want データをグラフとして可視化する機能, so that データの傾向やパターンを視覚的に理解できる

#### Acceptance Criteria
1. When 1次元配列が選択された場合, the Visualizerスクリプト shall 折れ線グラフまたは棒グラフを生成する
2. When 2次元配列が選択された場合, the Visualizerスクリプト shall ヒートマップ、散布図、または3Dサーフェスプロットを生成する
3. The Visualizerスクリプト shall グラフタイトル、軸ラベル、凡例を設定可能にする
4. The Visualizerスクリプト shall グラフの色、線のスタイル、マーカーをカスタマイズ可能にする
5. When グラフ生成が完了した場合, the Visualizerスクリプト shall グラフを画面に表示する

### Requirement 3: データ可視化機能
**Objective:** As a データアナリスト, I want 多様な可視化方法を選択できる機能, so that データの特性に応じた最適な表現を選べる

#### Acceptance Criteria
1. The Visualizerスクリプト shall 以下の可視化タイプをサポートする: 折れ線グラフ、散布図、棒グラフ、ヒストグラム、ヒートマップ、3Dプロット
2. When ユーザーが可視化タイプを選択した場合, the Visualizerスクリプト shall 選択されたタイプで適切に描画する
3. If データの次元が選択された可視化タイプと互換性がない場合, then the Visualizerスクリプト shall 警告を表示し、代替案を提案する
4. The Visualizerスクリプト shall 複数のサブプロットを同一画面に配置する機能を提供する
5. The Visualizerスクリプト shall 生成したグラフを画像ファイル（PNG、SVG、PDF）として保存する機能を提供する

### Requirement 4: データ分析機能
**Objective:** As a データアナリスト, I want データの統計情報を取得する機能, so that データの基本的な特性を数値で把握できる

#### Acceptance Criteria
1. The Visualizerスクリプト shall 基本統計量（平均、中央値、標準偏差、最小値、最大値）を計算し表示する
2. When ユーザーが統計分析を要求した場合, the Visualizerスクリプト shall データの分布特性（歪度、尖度）を計算する
3. The Visualizerスクリプト shall データの欠損値やNaN値の数を検出し報告する
4. Where 2次元データが提供された場合, the Visualizerスクリプト shall 相関行列を計算し可視化する
5. The Visualizerスクリプト shall 分析結果をテキスト形式またはCSV形式で出力する機能を提供する

### Requirement 5: 拡大表示・インタラクティブ機能
**Objective:** As a データアナリスト, I want グラフの特定領域を拡大表示する機能, so that 詳細なデータパターンを調査できる

#### Acceptance Criteria
1. When ユーザーがグラフ上の領域を選択した場合, the Visualizerスクリプト shall 選択された領域を拡大表示する
2. The Visualizerスクリプト shall マウスホイールまたはピンチジェスチャーによるズーム機能を提供する
3. While グラフが表示されている間, the Visualizerスクリプト shall パン（ドラッグによる移動）機能を提供する
4. When ユーザーがデータポイントにカーソルを合わせた場合, the Visualizerスクリプト shall そのポイントの座標値や属性情報をツールチップで表示する
5. The Visualizerスクリプト shall 拡大表示の状態をリセットして元の表示に戻す機能を提供する

### Requirement 6: ユーザーインターフェース
**Objective:** As a データアナリスト, I want 使いやすいコマンドラインまたはGUIインターフェース, so that 効率的にツールを操作できる

#### Acceptance Criteria
1. The Visualizerスクリプト shall コマンドライン引数でファイルパスと基本オプションを受け取る機能を提供する
2. When スクリプトが引数なしで起動された場合, the Visualizerスクリプト shall 使用方法のヘルプメッセージを表示する
3. If 無効な引数が渡された場合, then the Visualizerスクリプト shall エラーメッセージと正しい使用例を表示する
4. The Visualizerスクリプト shall インタラクティブモードで操作可能なメニューまたはGUIを提供する
5. The Visualizerスクリプト shall ユーザーの操作履歴や設定を保存・復元する機能を提供する

### Requirement 7: パフォーマンスとエラーハンドリング
**Objective:** As a データアナリスト, I want 大規模データでも安定して動作する機能, so that 実用的なデータ分析作業を遂行できる

#### Acceptance Criteria
1. The Visualizerスクリプト shall 100万要素以上のNumpy配列を5秒以内に読み込む
2. While 大規模データを処理している間, the Visualizerスクリプト shall 処理進捗状況を表示する
3. If メモリ不足やその他のシステムエラーが発生した場合, then the Visualizerスクリプト shall 適切なエラーメッセージを表示し、安全に終了する
4. The Visualizerスクリプト shall データ処理中に発生した例外をログファイルに記録する
5. The Visualizerスクリプト shall 異常終了時にデータの損失を防ぐための自動保存機能を提供する

### Requirement 8: 周波数解析・振幅スペクトル描画機能
**Objective:** As a データアナリスト, I want 時系列データの周波数成分を分析する機能, so that データに含まれる周期的なパターンや周波数特性を把握できる

#### Acceptance Criteria
1. The Visualizerスクリプト shall 1次元データに対してFFT（高速フーリエ変換）を実行する機能を提供する
2. When ユーザーがデータ範囲を指定した場合, the Visualizerスクリプト shall 指定された範囲のデータのみを切り抜いてFFT処理を行う
3. The Visualizerスクリプト shall FFT実行前にゼロパディング機能を提供し、パディングサイズをユーザーが設定可能にする
4. The Visualizerスクリプト shall FFT結果から振幅スペクトルを計算し、グラフとして描画する機能を提供する
5. When 振幅スペクトルを描画する場合, the Visualizerスクリプト shall 横軸に周波数、縦軸に振幅を表示する
6. The Visualizerスクリプト shall 振幅スペクトルの表示範囲（周波数範囲）をユーザーが設定可能にする
7. The Visualizerスクリプト shall 対数スケール表示オプションを提供する
8. If データ範囲が指定されていない場合, then the Visualizerスクリプト shall データ全体に対してFFT処理を実行する

