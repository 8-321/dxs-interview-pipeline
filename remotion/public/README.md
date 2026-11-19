# public/ 需要自备的素材

仓库不包含任何图片、字体、视频和音乐。渲染前按下面结构放进来：

```
public/
  clips/
    demo.mp4          # 1920x1080 / 24fps，timeline 里 src 指向它
  fonts/
    YouShe.ttf        # 优设标题黑（官方渠道下载）
    NotoSC.ttf        # 思源黑体
    Quicksand.ttf
    Bebas.ttf
    DDINCond.ttf
    Oswald.ttf
    NotoSerifSC.ttf
    MaShanZheng.ttf
    FusionPixel12.woff2
  music/
    bed.mp3           # 垫底音乐，注意授权
  logos/              # 片中用到的品牌 Logo
  plates/             # 底图
```

字体缺省时 `lib.tsx` 会回退到系统字体，但标题的斜切效果会丢失。
