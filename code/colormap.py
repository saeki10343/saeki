import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# 計測データ（例：5行×4列）　論文まで時間なかったのでデータ直打ち
temperature_data = np.array([
    [1.1912, 1.2198, 1.3076, 1.2502], #A
    [1.0047, 1.0244, 1.1263, 1.0456], #B
    [1.0476, 1.0329, 1.1706, 1.02], #C
    [1.0214, 1.0689, 1.0277, 0.9335], #D
    [0.9115, 1.0625, 1.0175, 0.9531], #E
])

# 元の計測点の位置（縦と横）
original_y = np.linspace(0, 16, 5)  # 縦方向（0mから20mを5点で分割）
original_x = np.linspace(0, 0.9, 4)  # 横方向（0mから90cmを4点で分割）

# 補間後の位置（縦10cm間隔、横1cm間隔）
new_y = np.linspace(0, 16, 201)  # 縦方向（0mから20mを10cm間隔で分割）
new_x = np.linspace(0, 0.9, 91)  # 横方向（0mから90cmを1cm間隔で分割）

# 2次元線形補間
interpolator = interp2d(original_x, original_y, temperature_data, kind='linear')
interpolated_data = interpolator(new_x, new_y)

# カラーマップの描画
plt.figure(figsize=(14, 8))
im = plt.imshow(interpolated_data, cmap="viridis", origin="lower",
                extent=[0, 0.9, 0, 16], aspect="auto")  # extentで実際の距離を指定
cbar = plt.colorbar(im, label="VPD (kPa)")  # カラーバーを取得

# カラーバーのフォントサイズを変更
cbar.ax.tick_params(labelsize=18)  # カラーバーの目盛りフォントサイズ
cbar.set_label("VPD (kPa)", fontsize=16)  # カラーバーのラベルフォントサイズ

# ラベルリスト（A1, A2, ..., E4）
row_labels = ["A", "B", "C", "D", "E"]
col_labels = ["1", "2", "3", "4"]

# 計測点をプロット（赤い点とラベルを追加）
for row_idx, y in enumerate(original_y):
    for col_idx, x in enumerate(original_x):
        plt.plot(x, y, 'o', color='red', markersize=6, label="Measurement Points")  # 計測点のプロット

# 縦軸（A～E）の設定
for i, label in enumerate(row_labels):
    plt.text(-0.05, original_y[i]+0.35, label, ha="center", va="center", fontsize=25, color="black", transform=plt.gca().transData)


# 横軸（1～4）の設定
for i, label in enumerate(col_labels):
    plt.text(original_x[i], -0.8, label, ha="center", va="center", fontsize=25, color="black", transform=plt.gca().transData)



# 軸ラベル設定
xticks = np.arange(0, 1.0, 0.3)  # 0mから0.9mまでを0.3m間隔
plt.xticks(ticks=xticks, labels=[f"{x:.1f}m" for x in xticks], fontsize=20)
plt.yticks(ticks=np.linspace(0, 16, 5), labels=[f"{y:.0f}m" for y in np.linspace(0, 16, 5)],fontsize=20)

plt.title("VPD Colormap",fontsize=20)
plt.xlabel("Width (m)",fontsize=16)
plt.ylabel("Depth (m)",fontsize=16)

# 重複ラベルを回避
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc="upper right",fontsize=16)

plt.show()