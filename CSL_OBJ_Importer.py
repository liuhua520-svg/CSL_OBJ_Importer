# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 liuhua520-svg
# URL: https://github.com/liuhua520-svg/CSL_OBJ_Importer

bl_info = {
    "name": "Cities Skylines OBJ Importer",
    "author": "liuhua520-svg",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "File > Import",
    "description": "Import Cities Skylines OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix",
    "category": "Import-Export",
}

import bpy
import os
import bmesh
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

# ====================== 多語言翻譯支援 (12種語言) ======================
# 已全部使用普通字串（無 _()），徹底解決 Blender 4.4 「name '_' is not defined」錯誤
translations_dict = {
    "zh_HANS": { # 簡體中文（你指定的「都市：天际线」）
        ("*", "Cities Skylines OBJ Importer"): "都市：天际线 OBJ 导入器",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "导入 OBJ + 自动匹配贴图(_d _a _c _i _n _s) + 可选导入 + X轴翻转 + _a透明完美修复",
        ("*", "Import CSL OBJ"): "导入都市：天际线 OBJ",
        ("*", "Cities Skylines OBJ with Texture Detection"): "都市：天际线 OBJ（带贴图自动检测）",
        ("*", "Import _d (Diffuse)"): "导入 _d (漫反射)",
        ("*", "Import diffuse texture (_d)"): "导入 diffuse 贴图 (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "导入 _a (透明)",
        ("*", "Import alpha transparency texture (_a)"): "导入 alpha 透明贴图 (_a)",
        ("*", "Import _c (Color Variation)"): "导入 _c (颜色变化)",
        ("*", "Import color variation mask (_c)"): "导入 color variation 遮罩 (_c)",
        ("*", "Import _i (Illumination/Emission)"): "导入 _i (自发光)",
        ("*", "Import illumination texture (_i)"): "导入 illumination 贴图 (_i)",
        ("*", "Import _n (Normal Map)"): "导入 _n (法线)",
        ("*", "Import normal map (_n)"): "导入 normal map (_n)",
        ("*", "Import _s (Specular)"): "导入 _s (高光)",
        ("*", "Import specular texture (_s)"): "导入 specular 贴图 (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "反转 X 轴 (镜像修正)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "干净翻转顶点 + 法线",
        ("*", "Delete Negative Z Vertices"): "删除负 Z 坐标顶点",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "删除 Z 坐标小于 0 的顶点（Z = 0 的顶点保留）",
    },
    "zh_TW": { # 繁體中文（台灣，你指定的「大都會：天際線」）
        ("*", "Cities Skylines OBJ Importer"): "大都會：天際線 OBJ 匯入器",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "匯入 OBJ + 自動匹配貼圖(_d _a _c _i _n _s) + 可選匯入 + X軸翻轉 + _a透明完美修復",
        ("*", "Import CSL OBJ"): "匯入大都會：天際線 OBJ",
        ("*", "Cities Skylines OBJ with Texture Detection"): "大都會：天際線 OBJ（帶貼圖自動偵測）",
        ("*", "Import _d (Diffuse)"): "匯入 _d (漫反射)",
        ("*", "Import diffuse texture (_d)"): "匯入 diffuse 貼圖 (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "匯入 _a (透明)",
        ("*", "Import alpha transparency texture (_a)"): "匯入 alpha 透明貼圖 (_a)",
        ("*", "Import _c (Color Variation)"): "匯入 _c (顏色變化)",
        ("*", "Import color variation mask (_c)"): "匯入 color variation 遮罩 (_c)",
        ("*", "Import _i (Illumination/Emission)"): "匯入 _i (自發光)",
        ("*", "Import illumination texture (_i)"): "匯入 illumination 貼圖 (_i)",
        ("*", "Import _n (Normal Map)"): "匯入 _n (法線)",
        ("*", "Import normal map (_n)"): "匯入 normal map (_n)",
        ("*", "Import _s (Specular)"): "匯入 _s (高光)",
        ("*", "Import specular texture (_s)"): "匯入 specular 貼圖 (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "反轉 X 軸 (鏡像修正)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "乾淨翻轉頂點 + 法線",
        ("*", "Delete Negative Z Vertices"): "刪除負 Z 座標頂點",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "刪除 Z 座標小於 0 的頂點（Z = 0 的頂點保留）",
    },
    "ja_JP": {
        ("*", "Cities Skylines OBJ Importer"): "シティーズ：スカイライン OBJ インポーター",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "OBJ をインポート + テクスチャ自動検出 (_d _a _c _i _n _s) + オプション + X軸反転 + α完全修正",
        ("*", "Import CSL OBJ"): "シティーズ：スカイライン OBJ をインポート",
        ("*", "Cities Skylines OBJ with Texture Detection"): "テクスチャ自動検出付きシティーズ：スカイライン OBJ",
        ("*", "Import _d (Diffuse)"): "_d をインポート (ディフューズ)",
        ("*", "Import diffuse texture (_d)"): "ディフューズテクスチャ (_d) をインポート",
        ("*", "Import _a (Alpha/Transparency)"): "_a をインポート (透明)",
        ("*", "Import alpha transparency texture (_a)"): "アルファ透明テクスチャ (_a) をインポート",
        ("*", "Import _c (Color Variation)"): "_c をインポート (カラー変化)",
        ("*", "Import color variation mask (_c)"): "カラー変化マスク (_c) をインポート",
        ("*", "Import _i (Illumination/Emission)"): "_i をインポート (発光)",
        ("*", "Import illumination texture (_i)"): "イルミネーションテクスチャ (_i) をインポート",
        ("*", "Import _n (Normal Map)"): "_n をインポート (ノーマルマップ)",
        ("*", "Import normal map (_n)"): "ノーマルマップ (_n) をインポート",
        ("*", "Import _s (Specular)"): "_s をインポート (スペキュラー)",
        ("*", "Import specular texture (_s)"): "スペキュラーテクスチャ (_s) をインポート",
        ("*", "Flip X Axis (Mirror Fix)"): "X軸反転 (ミラー修正)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "頂点反転 + 法線修正 (負スケールなし)",
        ("*", "Delete Negative Z Vertices"): "負のZ座標の頂点を削除",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Z座標が0未満の頂点を削除 (Z = 0 の頂点は残す)",
    },
    "fr_FR": {
        ("*", "Cities Skylines OBJ Importer"): "Importeur OBJ Cities Skylines",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "Importer OBJ + détection auto des textures (_d _a _c _i _n _s) + import optionnel + inversion X + correction alpha parfaite",
        ("*", "Import CSL OBJ"): "Importer OBJ Cities Skylines",
        ("*", "Cities Skylines OBJ with Texture Detection"): "OBJ Cities Skylines avec Détection de Textures",
        ("*", "Import _d (Diffuse)"): "Importer _d (Diffus)",
        ("*", "Import diffuse texture (_d)"): "Importer texture diffuse (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "Importer _a (Alpha/Transparence)",
        ("*", "Import alpha transparency texture (_a)"): "Importer texture alpha/transparence (_a)",
        ("*", "Import _c (Color Variation)"): "Importer _c (Variation de Couleur)",
        ("*", "Import color variation mask (_c)"): "Importer masque de variation de couleur (_c)",
        ("*", "Import _i (Illumination/Emission)"): "Importer _i (Illumination/Émission)",
        ("*", "Import illumination texture (_i)"): "Importer texture d'illumination (_i)",
        ("*", "Import _n (Normal Map)"): "Importer _n (Normal Map)",
        ("*", "Import normal map (_n)"): "Importer normal map (_n)",
        ("*", "Import _s (Specular)"): "Importer _s (Spéculaire)",
        ("*", "Import specular texture (_s)"): "Importer texture spéculaire (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "Inverser Axe X (Correction Miroir)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Inversion propre des sommets + normales (pas d'échelle négative)",
        ("*", "Delete Negative Z Vertices"): "Supprimer les sommets à Z négatif",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Supprimer les sommets dont Z < 0 (les sommets à Z = 0 sont conservés)",
    },
    "de_DE": {
        ("*", "Cities Skylines OBJ Importer"): "Cities Skylines OBJ-Importer",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "OBJ importieren + automatische Texturerkennung (_d _a _c _i _n _s) + optionaler Import + X-Achsen-Flip + perfekte Alpha-Korrektur",
        ("*", "Import CSL OBJ"): "Cities Skylines OBJ importieren",
        ("*", "Cities Skylines OBJ with Texture Detection"): "Cities Skylines OBJ mit Texturerkennung",
        ("*", "Import _d (Diffuse)"): "_d importieren (Diffuse)",
        ("*", "Import diffuse texture (_d)"): "Diffuse-Textur (_d) importieren",
        ("*", "Import _a (Alpha/Transparency)"): "_a importieren (Alpha/Transparenz)",
        ("*", "Import alpha transparency texture (_a)"): "Alpha-Transparenz-Textur (_a) importieren",
        ("*", "Import _c (Color Variation)"): "_c importieren (Farbvariation)",
        ("*", "Import color variation mask (_c)"): "Farbvariationsmaske (_c) importieren",
        ("*", "Import _i (Illumination/Emission)"): "_i importieren (Beleuchtung/Emission)",
        ("*", "Import illumination texture (_i)"): "Beleuchtungs-Textur (_i) importieren",
        ("*", "Import _n (Normal Map)"): "_n importieren (Normal Map)",
        ("*", "Import normal map (_n)"): "Normal Map (_n) importieren",
        ("*", "Import _s (Specular)"): "_s importieren (Specular)",
        ("*", "Import specular texture (_s)"): "Specular-Textur (_s) importieren",
        ("*", "Flip X Axis (Mirror Fix)"): "X-Achse umkehren (Spiegelkorrektur)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Sauberes Vertex-Flip + Normalen (keine negative Skalierung)",
        ("*", "Delete Negative Z Vertices"): "Vertices mit negativem Z löschen",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Vertices mit Z < 0 löschen (Vertices mit Z = 0 bleiben erhalten)",
    },
    "es_ES": {
        ("*", "Cities Skylines OBJ Importer"): "Importador OBJ Cities Skylines",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "Importar OBJ + detección automática de texturas (_d _a _c _i _n _s) + importación opcional + volteo X + corrección alpha perfecta",
        ("*", "Import CSL OBJ"): "Importar OBJ Cities Skylines",
        ("*", "Cities Skylines OBJ with Texture Detection"): "OBJ Cities Skylines con Detección de Texturas",
        ("*", "Import _d (Diffuse)"): "Importar _d (Difuso)",
        ("*", "Import diffuse texture (_d)"): "Importar textura difusa (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "Importar _a (Alfa/Transparencia)",
        ("*", "Import alpha transparency texture (_a)"): "Importar textura alpha/transparencia (_a)",
        ("*", "Import _c (Color Variation)"): "Importar _c (Variación de Color)",
        ("*", "Import color variation mask (_c)"): "Importar máscara de variación de color (_c)",
        ("*", "Import _i (Illumination/Emission)"): "Importar _i (Iluminación/Emisión)",
        ("*", "Import illumination texture (_i)"): "Importar textura de iluminación (_i)",
        ("*", "Import _n (Normal Map)"): "Importar _n (Normal Map)",
        ("*", "Import normal map (_n)"): "Importar normal map (_n)",
        ("*", "Import _s (Specular)"): "Importar _s (Especular)",
        ("*", "Import specular texture (_s)"): "Importar textura especular (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "Invertir Eje X (Corrección de Espejo)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Volteo limpio de vértices + normales (sin escala negativa)",
        ("*", "Delete Negative Z Vertices"): "Eliminar vértices con Z negativa",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Eliminar vértices con Z < 0 (se conservan los de Z = 0)",
    },
    "pl_PL": {
        ("*", "Cities Skylines OBJ Importer"): "Importer OBJ Cities Skylines",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "Importuj OBJ + automatyczne wykrywanie tekstur (_d _a _c _i _n _s) + import opcjonalny + odwrócenie X + idealna korekta alpha",
        ("*", "Import CSL OBJ"): "Importuj OBJ Cities Skylines",
        ("*", "Cities Skylines OBJ with Texture Detection"): "OBJ Cities Skylines z wykrywaniem tekstur",
        ("*", "Import _d (Diffuse)"): "Importuj _d (Diffuse)",
        ("*", "Import diffuse texture (_d)"): "Importuj teksturę diffuse (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "Importuj _a (Alpha/Przezroczystość)",
        ("*", "Import alpha transparency texture (_a)"): "Importuj teksturę alpha/przezroczystość (_a)",
        ("*", "Import _c (Color Variation)"): "Importuj _c (Zmiana Koloru)",
        ("*", "Import color variation mask (_c)"): "Importuj maskę zmiany koloru (_c)",
        ("*", "Import _i (Illumination/Emission)"): "Importuj _i (Iluminacja/Emisja)",
        ("*", "Import illumination texture (_i)"): "Importuj teksturę iluminacji (_i)",
        ("*", "Import _n (Normal Map)"): "Importuj _n (Normal Map)",
        ("*", "Import normal map (_n)"): "Importuj normal map (_n)",
        ("*", "Import _s (Specular)"): "Importuj _s (Specular)",
        ("*", "Import specular texture (_s)"): "Importuj teksturę specular (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "Odwróć oś X (Korekta lustra)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Czyste odwrócenie wierzchołków + normalne (bez negatywnej skali)",
        ("*", "Delete Negative Z Vertices"): "Usuń wierzchołki z ujemnym Z",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Usuń wierzchołki z Z < 0 (wierzchołki z Z = 0 pozostają)",
    },
    "pt_BR": {
        ("*", "Cities Skylines OBJ Importer"): "Importador OBJ Cities Skylines",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "Importar OBJ + detecção automática de texturas (_d _a _c _i _n _s) + importação opcional + inversão X + correção alpha perfeita",
        ("*", "Import CSL OBJ"): "Importar OBJ Cities Skylines",
        ("*", "Cities Skylines OBJ with Texture Detection"): "OBJ Cities Skylines com Detecção de Texturas",
        ("*", "Import _d (Diffuse)"): "Importar _d (Difuso)",
        ("*", "Import diffuse texture (_d)"): "Importar textura difusa (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "Importar _a (Alpha/Transparência)",
        ("*", "Import alpha transparency texture (_a)"): "Importar textura alpha/transparência (_a)",
        ("*", "Import _c (Color Variation)"): "Importar _c (Variação de Cor)",
        ("*", "Import color variation mask (_c)"): "Importar máscara de variação de cor (_c)",
        ("*", "Import _i (Illumination/Emission)"): "Importar _i (Iluminação/Emissão)",
        ("*", "Import illumination texture (_i)"): "Importar textura de iluminação (_i)",
        ("*", "Import _n (Normal Map)"): "Importar _n (Normal Map)",
        ("*", "Import normal map (_n)"): "Importar normal map (_n)",
        ("*", "Import _s (Specular)"): "Importar _s (Especular)",
        ("*", "Import specular texture (_s)"): "Importar textura especular (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "Inverter Eixo X (Correção de Espelho)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Inversão limpa de vértices + normais (sem escala negativa)",
        ("*", "Delete Negative Z Vertices"): "Excluir vértices com Z negativo",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Excluir vértices com Z < 0 (vértices com Z = 0 são mantidos)",
    },
    "ru_RU": {
        ("*", "Cities Skylines OBJ Importer"): "Импортер OBJ Cities Skylines",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "Импортировать OBJ + автоопределение текстур (_d _a _c _i _n _s) + опциональный импорт + переворот X + идеальная коррекция alpha",
        ("*", "Import CSL OBJ"): "Импортировать OBJ Cities Skylines",
        ("*", "Cities Skylines OBJ with Texture Detection"): "OBJ Cities Skylines с определением текстур",
        ("*", "Import _d (Diffuse)"): "Импортировать _d (Диффузный)",
        ("*", "Import diffuse texture (_d)"): "Импортировать диффузную текстуру (_d)",
        ("*", "Import _a (Alpha/Transparency)"): "Импортировать _a (Альфа/Прозрачность)",
        ("*", "Import alpha transparency texture (_a)"): "Импортировать альфа-текстуру прозрачности (_a)",
        ("*", "Import _c (Color Variation)"): "Импортировать _c (Вариация цвета)",
        ("*", "Import color variation mask (_c)"): "Импортировать маску вариации цвета (_c)",
        ("*", "Import _i (Illumination/Emission)"): "Импортировать _i (Освещение/Эмиссия)",
        ("*", "Import illumination texture (_i)"): "Импортировать текстуру освещения (_i)",
        ("*", "Import _n (Normal Map)"): "Импортировать _n (Normal Map)",
        ("*", "Import normal map (_n)"): "Импортировать normal map (_n)",
        ("*", "Import _s (Specular)"): "Импортировать _s (Specular)",
        ("*", "Import specular texture (_s)"): "Импортировать спекулярную текстуру (_s)",
        ("*", "Flip X Axis (Mirror Fix)"): "Перевернуть ось X (Исправление зеркала)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Чистый переворот вершин + нормали (без отрицательной шкалы)",
        ("*", "Delete Negative Z Vertices"): "Удалить вершины с отрицательным Z",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Удалить вершины с Z < 0 (вершины с Z = 0 сохраняются)",
    },
    "ko_KR": {
        ("*", "Cities Skylines OBJ Importer"): "시티즈: 스카이라인 OBJ 임포터",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "OBJ 가져오기 + 자동 텍스처 감지 (_d _a _c _i _n _s) + 선택적 가져오기 + X축 뒤집기 + 완벽한 알파 수정",
        ("*", "Import CSL OBJ"): "시티즈: 스카이라인 OBJ 가져오기",
        ("*", "Cities Skylines OBJ with Texture Detection"): "텍스처 자동 감지 시티즈: 스카이라인 OBJ",
        ("*", "Import _d (Diffuse)"): "_d 가져오기 (Diffuse)",
        ("*", "Import diffuse texture (_d)"): "Diffuse 텍스처 (_d) 가져오기",
        ("*", "Import _a (Alpha/Transparency)"): "_a 가져오기 (알파/투명도)",
        ("*", "Import alpha transparency texture (_a)"): "알파 투명도 텍스처 (_a) 가져오기",
        ("*", "Import _c (Color Variation)"): "_c 가져오기 (색상 변화)",
        ("*", "Import color variation mask (_c)"): "색상 변화 마스크 (_c) 가져오기",
        ("*", "Import _i (Illumination/Emission)"): "_i 가져오기 (조명/발광)",
        ("*", "Import illumination texture (_i)"): "조명 텍스처 (_i) 가져오기",
        ("*", "Import _n (Normal Map)"): "_n 가져오기 (노멀 맵)",
        ("*", "Import normal map (_n)"): "노멀 맵 (_n) 가져오기",
        ("*", "Import _s (Specular)"): "_s 가져오기 (스페큘러)",
        ("*", "Import specular texture (_s)"): "스페큘러 텍스처 (_s) 가져오기",
        ("*", "Flip X Axis (Mirror Fix)"): "X축 뒤집기 (미러 수정)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "정확한 버텍스 뒤집기 + 노멀 (음수 스케일 없음)",
        ("*", "Delete Negative Z Vertices"): "음수 Z 좌표 버텍스 삭제",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Z 좌표가 0 미만인 버텍스 삭제 (Z = 0 버텍스는 유지)",
    },
    "tr_TR": {
        ("*", "Cities Skylines OBJ Importer"): "Cities Skylines OBJ İçe Aktarıcı",
        ("*", "Import OBJ with auto texture detection (_d _a _c _i _n _s) + optional import + X-axis flip + perfect alpha fix"): "OBJ İçe Aktar + otomatik doku algılama (_d _a _c _i _n _s) + opsiyonel içe aktarma + X ekseni çevir + mükemmel alpha düzeltme",
        ("*", "Import CSL OBJ"): "Cities Skylines OBJ İçe Aktar",
        ("*", "Cities Skylines OBJ with Texture Detection"): "Doku Algılama Özelliği Olan Cities Skylines OBJ",
        ("*", "Import _d (Diffuse)"): "_d İçe Aktar (Diffuse)",
        ("*", "Import diffuse texture (_d)"): "Diffuse doku (_d) içe aktar",
        ("*", "Import _a (Alpha/Transparency)"): "_a İçe Aktar (Alpha/Şeffaflık)",
        ("*", "Import alpha transparency texture (_a)"): "Alpha şeffaflık dokusu (_a) içe aktar",
        ("*", "Import _c (Color Variation)"): "_c İçe Aktar (Renk Değişimi)",
        ("*", "Import color variation mask (_c)"): "Renk değişim maskesi (_c) içe aktar",
        ("*", "Import _i (Illumination/Emission)"): "_i İçe Aktar (Işık/Yayma)",
        ("*", "Import illumination texture (_i)"): "Işık dokusu (_i) içe aktar",
        ("*", "Import _n (Normal Map)"): "_n İçe Aktar (Normal Map)",
        ("*", "Import normal map (_n)"): "Normal map (_n) içe aktar",
        ("*", "Import _s (Specular)"): "_s İçe Aktar (Specular)",
        ("*", "Import specular texture (_s)"): "Specular doku (_s) içe aktar",
        ("*", "Flip X Axis (Mirror Fix)"): "X Ekseni Çevir (Ayna Düzeltme)",
        ("*", "Clean vertex flip + normals (no negative scale)"): "Temiz vertex çevirme + normal (negatif ölçek yok)",
        ("*", "Delete Negative Z Vertices"): "Negatif Z Köşelerini Sil",
        ("*", "Delete vertices with Z < 0 (vertices with Z = 0 are kept)"): "Z < 0 olan köşeleri sil (Z = 0 olanlar korunur)",
    },
}

# ====================== 貼圖搜尋 & 材質建立 ======================
def find_texture(folder, base_name, suffix):
    base_lower = base_name.lower()
    suffix_lower = suffix.lower()
    exact_name = base_name + suffix + ".png"
    for f in os.listdir(folder):
        if f.lower() == exact_name.lower():
            return os.path.join(folder, f)
    for f in os.listdir(folder):
        if f.lower().endswith(".png"):
            stem = os.path.splitext(f)[0].lower()
            if stem.startswith(base_lower) and suffix_lower in stem:
                return os.path.join(folder, f)
    return None

def create_material(obj, folder, base_name,
                    import_d, import_a, import_c, import_i, import_n, import_s):
    mat = bpy.data.materials.new(name=f"{obj.name}_mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    output = nodes.new(type="ShaderNodeOutputMaterial")
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    def add_tex(path, noncolor=False):
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(path)
        if noncolor:
            tex.image.colorspace_settings.name = "Non-Color"
        return tex

    if import_d:
        diff = find_texture(folder, base_name, "_d")
        if diff:
            tex = add_tex(diff)
            links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])

    if import_a:
        alpha = find_texture(folder, base_name, "_a")
        if alpha:
            tex = add_tex(alpha, True)
            links.new(tex.outputs["Color"], bsdf.inputs["Alpha"])
            mat.blend_method = 'CLIP'
            try:
                mat.shadow_method = 'HASHED'
            except:
                pass

    if import_c:                                      # ← 這裡已修正為標準寫法
        col = find_texture(folder, base_name, "_c")
        if col:
            tex = add_tex(col, True)

    if import_i:
        illum = find_texture(folder, base_name, "_i")
        if illum:
            tex = add_tex(illum, True)
            if "Emission Color" in bsdf.inputs:
                links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
            elif "Emission" in bsdf.inputs:
                links.new(tex.outputs["Color"], bsdf.inputs["Emission"])

    if import_s:
        spec = find_texture(folder, base_name, "_s")
        if spec:
            tex = add_tex(spec, True)
            if "Specular" in bsdf.inputs:
                links.new(tex.outputs["Color"], bsdf.inputs["Specular"])

    if import_n:
        norm = find_texture(folder, base_name, "_n")
        if norm:
            tex = add_tex(norm, True)
            nmap = nodes.new("ShaderNodeNormalMap")
            links.new(tex.outputs["Color"], nmap.inputs["Color"])
            links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])

    obj.data.materials.clear()
    obj.data.materials.append(mat)

# ====================== 支援多檔匯入 ======================
class IMPORT_OT_special_obj(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.special_obj"
    bl_label = "Import CSL OBJ"

    filename_ext = ".obj"
    filter_glob: StringProperty(default="*.obj", options={'HIDDEN'})

    directory: StringProperty(subtype='DIR_PATH', options={'HIDDEN'})
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'}
    )

    import_d: BoolProperty(name="Import _d (Diffuse)", description="Import diffuse texture (_d)", default=True)
    import_a: BoolProperty(name="Import _a (Alpha/Transparency)", description="Import alpha transparency texture (_a)", default=True)
    import_c: BoolProperty(name="Import _c (Color Variation)", description="Import color variation mask (_c)", default=True)
    import_i: BoolProperty(name="Import _i (Illumination/Emission)", description="Import illumination texture (_i)", default=True)
    import_n: BoolProperty(name="Import _n (Normal Map)", description="Import normal map (_n)", default=True)
    import_s: BoolProperty(name="Import _s (Specular)", description="Import specular texture (_s)", default=True)
    flip_x_axis: BoolProperty(name="Flip X Axis (Mirror Fix)", description="Clean vertex flip + normals (no negative scale)", default=False)
    delete_negative_z: BoolProperty(name="Delete Negative Z Vertices", description="Delete vertices with Z < 0 (vertices with Z = 0 are kept)", default=False)

    def execute(self, context):
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            base_name = os.path.splitext(file_elem.name)[0]

            bpy.ops.wm.obj_import(filepath=filepath)

            for obj in list(context.selected_objects):
                if obj.type == 'MESH':
                    create_material(obj, directory, base_name,
                                    self.import_d, self.import_a, self.import_c,
                                    self.import_i, self.import_n, self.import_s)
                    if self.flip_x_axis:
                        bm = bmesh.new()
                        bm.from_mesh(obj.data)
                        for v in bm.verts:
                            v.co.x *= -1
                        bmesh.ops.reverse_faces(bm, faces=bm.faces)
                        bm.to_mesh(obj.data)
                        bm.free()
                        obj.data.update()
                    if self.delete_negative_z:
                        # Blender 4.x 的 OBJ 导入器是用「物体旋转」做轴转换的，
                        # 顶点本地坐标仍是 OBJ 原始坐标，所以必须换算成世界坐标再判断 Z
                        context.view_layer.update()
                        mw = obj.matrix_world.copy()
                        bm = bmesh.new()
                        bm.from_mesh(obj.data)
                        # 仅删除世界 Z 严格小于 0 的顶点；Z = 0 的顶点保留（留出极小容差避免浮点误差）
                        neg_verts = [v for v in bm.verts if (mw @ v.co).z < -1e-6]
                        if neg_verts:
                            bmesh.ops.delete(bm, geom=neg_verts, context='VERTS')
                        bm.to_mesh(obj.data)
                        bm.free()
                        obj.data.update()
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_special_obj.bl_idname, text="Import Cities Skylines OBJ")

classes = (IMPORT_OT_special_obj,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.app.translations.register(__name__, translations_dict)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.app.translations.unregister(__name__)

if __name__ == "__main__":
    register()
