# Research & Design Decisions

---
**Purpose**: Capture discovery findings, architectural investigations, and rationale that inform the technical design.

**Usage**:
- Log research activities and outcomes during the discovery phase.
- Document design decision trade-offs that are too detailed for `design.md`.
- Provide references and evidence for future audits or reuse.
---

## Summary
- **Feature**: `numpy-data-visualizer`
- **Discovery Scope**: New Feature (Greenfield)
- **Key Findings**:
  - Matplotlib 3.10+はインタラクティブ機能とGPU高速化レンダリングをサポートし、科学的可視化に最適
  - scipy.fftは実信号処理に対してnumpy.fftより優れた機能とパフォーマンスを提供
  - argparseは標準ライブラリで軽量、外部依存なしのCLI開発に適している
  - モジュラーアーキテクチャ（データ/可視化/分析の分離）により保守性と拡張性が向上

## Research Log

### データ可視化ライブラリの選択

**Context**: 1次元データの可視化、インタラクティブ機能、グラフエクスポートをサポートするライブラリの選定

**Sources Consulted**:
- [Top 10 Python Data Visualization Libraries in 2025 - Reflex Blog](https://reflex.dev/blog/2025-01-27-top-10-data-visualization-libraries/)
- [Plotly vs Matplotlib in Python - Kanaries](https://docs.kanaries.net/articles/plotly-vs-matplotlib)
- [Matplotlib Interactive Figures Documentation](https://matplotlib.org/stable/users/explain/figure/interactive.html)

**Findings**:
- **Matplotlib**: 2025年のv3.10アップデートでGPU高速化レンダリング、ダークモードデフォルト、強化されたインタラクティブ機能を提供
- Matplotlibは静的・出版品質のプロットに優れ、NumPy/pandasとの統合が強力
- インタラクティブバックエンド（Qt、Tk、ipympl）を使用することで、ズーム、パン、ツールチップ機能を実現可能
- 組み込みナビゲーションツールバーがズーム、パン、リセット、保存機能を提供
- **Plotly**: ビジネスダッシュボードやWeb統合に強いが、本プロジェクトの科学的データ分析には過剰
- Matplotlibは以下の可視化タイプをネイティブサポート：折れ線、散布図、棒グラフ、ヒストグラム、ヒートマップ、3Dプロット

**Implications**:
- Matplotlibを主要可視化ライブラリとして選択
- インタラクティブバックエンド（Qt5Agg、TkAgg）を使用してズーム/パン機能を実装
- PNG、SVG、PDF形式のエクスポートをMatplotlibのネイティブ機能で実現

### FFTライブラリとベストプラクティス

**Context**: 1次元時系列データのFFT処理、振幅スペクトル計算、ゼロパディングの実装方針

**Sources Consulted**:
- [Fourier Transforms With scipy.fft - Real Python](https://realpython.com/python-scipy-fft/)
- [SciPy FFT Documentation](https://docs.scipy.org/doc/scipy/tutorial/fft.html)
- [NumPy FFT Documentation](https://numpy.org/doc/stable/reference/routines.fft.html)

**Findings**:
- **scipy.fft推奨**: NumPyのFFT実装より多機能で、バグ修正も頻繁、実世界の信号処理に最適
- **実信号処理**: 実数値データ（音声、センサーデータ）には`rfft`/`irfft`を使用することで計算時間が約半分に削減
- **ゼロパディング**: `next_fast_len()`を使用して最適なFFTサイズを計算し、パフォーマンスを向上
- **ウィンドウ関数**: 非周期的信号やウィンドウ化されたデータには、ハニング窓（`np.hanning`）を適用してスペクトル漏れを低減
- **周波数軸**: `scipy.fft.rfftfreq()`でサンプリングレート対応の正確な周波数軸を生成

**Implications**:
- scipy.fftモジュールを使用（`scipy.fft.rfft`, `scipy.fft.rfftfreq`）
- ユーザー指定可能なゼロパディング機能を実装
- ウィンドウ関数オプション（ハニング、ハミング、ブラックマン）を提供
- 振幅スペクトルは`np.abs(fft_result)`で計算

### インタラクティブプロット機能

**Context**: グラフのズーム、パン、ツールチップ表示の技術的実装方法

**Sources Consulted**:
- [Matplotlib Interactive Figures](https://matplotlib.org/stable/users/explain/figure/interactive.html)
- [Zooming and Panning - mpl-interactions](https://mpl-interactions.readthedocs.io/en/stable/examples/zoom-factory.html)

**Findings**:
- **インタラクティブバックエンド必須**: 静的バックエンド（Agg、inline）ではズーム/パン不可
- **推奨バックエンド**: Qt5Agg、TkAgg（デスクトップ）、widget（Jupyter）
- **組み込みナビゲーション**:
  - パン：左マウスボタンでドラッグ
  - ズーム：右マウスボタンで比例ズーム、またはマウスホイール
  - 修飾キー：`x`（x軸のみ）、`y`（y軸のみ）、`CONTROL`（アスペクト比保持）
- **ツールチップ**: `mplcursors`ライブラリまたはMatplotlibのアノテーション機能でカーソル位置の値を表示
- **リセット機能**: ツールバーの「Home」ボタンで元の表示に復帰

**Implications**:
- インタラクティブバックエンドを自動選択（利用可能性に基づく）
- Matplotlibの組み込みナビゲーションツールバーを活用
- `mplcursors`ライブラリでツールチップ機能を実装（オプション依存）
- プログラム的なズーム/パンAPIも提供（`ax.set_xlim()`, `ax.set_ylim()`）

### CLIアーキテクチャと設計パターン

**Context**: コマンドライン引数処理、ヘルプメッセージ、インタラクティブモードの設計

**Sources Consulted**:
- [Building Python CLI with Command Pattern - Medium](https://medium.com/@sasadangelo/building-a-python-command-line-interface-cli-with-the-command-pattern-f531b5d2a0fa)
- [Click vs argparse - Python Snacks](https://www.pythonsnacks.com/p/click-vs-argparse-python)
- [Build CLI with argparse - Real Python](https://realpython.com/command-line-interfaces-python-argparse/)

**Findings**:
- **argparse**: Python標準ライブラリ、外部依存なし、軽量プロジェクトに最適
- **click**: より洗練されたヘルプページ、ネストされたコマンド構造に強いが、外部依存が必要
- **コマンドパターン**: 各機能をコマンドクラスとして実装し、モジュラー性とテスト容易性を向上
- **MVCパターン適用**: CLIロジック、モデル（データ処理）、ビュー（表示）を分離
- **サブコマンドパターン**: Git/Docker風の`verb-noun`構造で関連機能をグループ化

**Implications**:
- argparseを使用（標準ライブラリ、依存なし）
- モジュラー設計：`data_loader.py`, `visualizer.py`, `analyzer.py`, `fft_processor.py`, `cli.py`
- コマンドパターンで機能を実装（load, plot, analyze, fft）
- インタラクティブモードはシンプルなメニューベースUI（`input()`ループ）

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| Monolithic Script | すべての機能を1つのファイルに実装 | シンプル、初期開発が高速 | 保守性低下、テスト困難、拡張性なし | 小規模プロジェクトには適するが、要件の複雑さから不適切 |
| Modular Architecture | データ処理、可視化、分析、FFT、CLIをモジュール分離 | 高い保守性、テスト容易、拡張性、並列開発可能 | 初期構造設計が必要 | **選択** - 要件の複雑さに適合 |
| MVC Pattern | Model（データ）、View（可視化）、Controller（CLI/ロジック）を分離 | 明確な責任分離、ビジネスロジックとUIの独立性 | Pythonスクリプトには過剰な抽象化 | MVCの原則を採用するが、厳格な実装は避ける |
| Plugin Architecture | プラグイン可能な可視化/分析モジュール | 高い拡張性、サードパーティ統合 | 複雑性増加、プラグインシステムのオーバーヘッド | 将来の拡張オプションとして検討 |

## Design Decisions

### Decision: `Matplotlib選択とPlotly却下`

**Context**: 要件1-3、5で求められるグラフ化、可視化、インタラクティブ機能を実現するライブラリの選定

**Alternatives Considered**:
1. **Matplotlib** - 科学的プロット、静的/インタラクティブ両対応、NumPy統合強力
2. **Plotly** - Web統合、ダッシュボード、ビジネス分析に強い
3. **Bokeh** - インタラクティブWebベース可視化、サーバー機能

**Selected Approach**: Matplotlib 3.10+

**Rationale**:
- 1次元データの科学的分析に最適化されており、要件の主対象に合致
- インタラクティブバックエンドで要件5（ズーム/パン）を満たす
- NumPy配列との直接統合により要件1のデータ読み込みがシームレス
- 標準的な可視化タイプ（折れ線、散布図、ヒートマップ、3D）を全てサポート
- PNG、SVG、PDFエクスポートがネイティブ対応（要件3.5）
- 外部依存が少なく、インストール・配布が容易

**Trade-offs**:
- **利点**: 安定性、豊富なドキュメント、科学コミュニティでの標準、出版品質
- **妥協点**: PlotlyのようなWebネイティブなインタラクティブ性は限定的（ただし要件には不要）

**Follow-up**: インタラクティブバックエンド（Qt5Agg、TkAgg）の自動選択ロジックを実装時に検証

### Decision: `scipy.fft採用とnumpy.fft非採用`

**Context**: 要件8で求められるFFT処理、振幅スペクトル計算の実装ライブラリ選定

**Alternatives Considered**:
1. **numpy.fft** - 標準ライブラリ、基本的なFFT機能
2. **scipy.fft** - より多機能、実信号最適化、パフォーマンス向上

**Selected Approach**: scipy.fft（特に`rfft`、`rfftfreq`）

**Rationale**:
- SciPy公式推奨：NumPyはFFT機能を後方互換性のために保持するが、SciPyへの移行を推奨
- 実信号処理に特化した`rfft`で計算時間を約50%削減（要件8の1次元データは実数値）
- `next_fast_len()`によるゼロパディング最適化（要件8.3）
- より頻繁なバグ修正とメンテナンス
- 周波数軸生成（`rfftfreq`）がサンプリングレート対応で正確

**Trade-offs**:
- **利点**: パフォーマンス、機能豊富、実信号最適化、保守性
- **妥協点**: scipy依存追加（ただしNumPyと同様に科学計算の標準依存）

**Follow-up**: ウィンドウ関数（ハニング、ハミング）の適用タイミングとデフォルト値を実装時に検証

### Decision: `argparse選択とclick非採用`

**Context**: 要件6で求められるCLI、ヘルプメッセージ、引数処理の実装方法

**Alternatives Considered**:
1. **argparse** - 標準ライブラリ、軽量、外部依存なし
2. **click** - 高機能、洗練されたヘルプ、ネストコマンド対応
3. **typer** - 型ヒント活用、現代的API

**Selected Approach**: argparse

**Rationale**:
- Python標準ライブラリで外部依存なし（配布・インストールが容易）
- 要件6のコマンドライン引数処理、ヘルプメッセージに十分な機能
- ネストされたサブコマンドは不要（シンプルなオプション構造）
- 科学計算分野での一般的な選択肢

**Trade-offs**:
- **利点**: 依存なし、標準化、軽量、十分な機能
- **妥協点**: clickのような洗練されたヘルプページやネストコマンドは不可（ただし要件には不要）

**Follow-up**: インタラクティブモードとCLIモードの統合方法を実装時に設計

### Decision: `モジュラーアーキテクチャ採用`

**Context**: 要件1-8の多様な機能（データ読み込み、可視化、分析、FFT、UI）を保守可能に実装する構造設計

**Alternatives Considered**:
1. **モノリシックスクリプト** - 1ファイルに全機能
2. **モジュラー設計** - 機能別モジュール分離
3. **厳格なMVC** - Model/View/Controllerの完全分離

**Selected Approach**: モジュラー設計（MVCの原則を採用、厳格な実装は避ける）

**Rationale**:
- 要件の複雑さ（8つの主要機能領域）にモノリシックは不適
- モジュール分離により並列開発、単体テスト、将来の拡張が容易
- 各モジュールの責任が明確：
  - `data_loader`: NumPy配列読み込み（要件1）
  - `visualizer`: グラフ生成、可視化（要件2, 3, 5）
  - `analyzer`: 統計分析（要件4）
  - `fft_processor`: FFT、振幅スペクトル（要件8）
  - `cli`: コマンドライン/インタラクティブUI（要件6）
- Pythonスクリプトとして適切な抽象化レベル

**Trade-offs**:
- **利点**: 保守性、テスト容易性、拡張性、チーム開発適合
- **妥協点**: 初期ファイル構造設計が必要（ただし長期的には投資対効果高）

**Follow-up**: モジュール間インターフェース（関数シグネチャ）を設計フェーズで明確化

## Risks & Mitigations

- **Risk 1: インタラクティブバックエンドの環境依存性** — Qt/Tkがインストールされていない環境でズーム/パン機能が動作しない
  - **Mitigation**: バックエンド自動選択ロジック実装、フォールバック機能（静的プロットでも基本機能は動作）、インストール手順ドキュメント化

- **Risk 2: 大規模データでのメモリ不足** — 100万要素超の配列でFFTやプロット時にメモリ枯渇
  - **Mitigation**: チャンク処理、データサンプリングオプション、メモリ使用量モニタリング、要件7.3のエラーハンドリング

- **Risk 3: FFTゼロパディングの誤用** — 不適切なパディングで周波数解析結果が歪む
  - **Mitigation**: `scipy.fft.next_fast_len()`使用、デフォルト値の適切な設定、ユーザーガイドでベストプラクティス説明

- **Risk 4: 複数可視化タイプの互換性チェック不足** — データ次元と可視化タイプの不一致でエラー
  - **Mitigation**: 要件3.3の検証ロジック実装、明確なエラーメッセージと代替案提示

## References
- [Top 10 Python Data Visualization Libraries in 2025 - Reflex Blog](https://reflex.dev/blog/2025-01-27-top-10-data-visualization-libraries/)
- [Plotly vs Matplotlib Comparison - Kanaries](https://docs.kanaries.net/articles/plotly-vs-matplotlib)
- [Matplotlib Interactive Figures Documentation](https://matplotlib.org/stable/users/explain/figure/interactive.html)
- [Fourier Transforms with scipy.fft - Real Python](https://realpython.com/python-scipy-fft/)
- [SciPy FFT Tutorial](https://docs.scipy.org/doc/scipy/tutorial/fft.html)
- [NumPy FFT Documentation](https://numpy.org/doc/stable/reference/routines.fft.html)
- [Building Python CLI with Command Pattern - Medium](https://medium.com/@sasadangelo/building-a-python-command-line-interface-cli-with-the-command-pattern-f531b5d2a0fa)
- [Build CLI with argparse - Real Python](https://realpython.com/command-line-interfaces-python-argparse/)
