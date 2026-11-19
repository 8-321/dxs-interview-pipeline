# 示例分镜：6 个场景，全部为虚构内容
# 用法：cd remotion && python story_core.py ../sample/timeline.demo.json ../sample/scenes_demo.py

HOST = dict(aroll='pip', pip='br', pipd=360, pipk=0.46, pfx=0.51, pfy=0.57)


def host(sc):
    return dict(HOST)


def title():
    T = G('TITLE')
    sc = Scene('title', T.t0, {'type': 'title'}, sway=0)
    sc.add('titlecard', T.t0 + 0.05, layer='screen', l1='大学生采访', l2='一份副业',
           l2b='从一个 AI 小工具开始', q='普通人能复制吗？', qSize=52, slam=0.7)
    sc.fx(T.t0 + 0.75, 'shake', a=16, d=0.32)
    show(sc, T.t0, T.t1)
    KF.append(('title', T.t0 + 2.2))


def who():
    A = G('S02')
    t0, t1 = A.t0, A.t1
    sc = Scene('who', t0, {'type': 'dark', 'v': 1})
    X, Y, cw, ch, gap = 960, 560, 600, 570, 48
    sc.cam(t0, x=960, y=560, s=1.0)
    sc.add('wall', t0 + 0.02, x=X, y=Y, cols=3, cw=cw, ch=ch, gap=gap, nodof=True, sfx='whoosh', cards=[
        dict(word='大三', size=230, ty=0.10, sub='某大学', ss=54, en='JUNIOR', es=24),
        dict(word='工科', size=230, ty=0.10, sub='工科专业', ss=50, en='ENGINEERING', es=22),
        dict(word='AI 小工具', size=120, ty=0.12, sub='一份副业', ss=48, en='SIDE PROJECT', es=22)],
        focus=[[t0, -1], [max(t0, A.k('大三', -0.2)), 0], [A.k('大学', -0.1), 1], [A.k('小A', -0.1), 2]])
    show(sc, t0, t1, **host(sc))
    KF.append(('who', t1 - 0.3))


def cost():
    A = G('S03')
    t0, t1 = A.t0, A.t1
    sc = Scene('cost', t0, {'type': 'dark', 'v': 3, 'particles': True})
    sc.cam(t0, x=930, y=500, s=1.12)
    sc.add('bignum', t0 + 0.02, x=880, y=500, v='200', count=[0, 200, 0], ct=t0 + 0.35, cd=0.9,
           size=540, unit='块', kicker='启动成本', cap='示例金额 · 虚构内容', anim='zoom', ad=0.5,
           nodof=True, sfx='kaching')
    sc.add('tag', t0 + 0.5, txt='≈ 一顿饭钱', x=1430, y=300, size=44)
    show(sc, t0, t1, **host(sc))
    KF.append(('cost', t1 - 0.3))


def income():
    A = G('S04')
    t0, t1 = A.t0, A.t1
    sc = Scene('income', t0, {'type': 'dark', 'v': 1})
    sc.cam(t0, x=900, y=540, s=1.0)
    sc.add('paper', t0 + 0.02, x=880, y=500, w=1640, h=860, kind='barh', title='做之前 / 做之后',
           kicker='示例数据 · 单位：元', unit='元', src='示例值，非真实收入', lw=300,
           rows=[dict(l='做之前', v=1500, out=True), dict(l='做之后', v=3000)],
           hi=[[t0, -1], [max(t0, A.k('生活费', -0.2)), 1]], anim='up', ad=0.6, rot=-2, nodof=True, sfx='whoosh')
    show(sc, t0, t1, **host(sc))
    KF.append(('income', t1 - 0.3))


def quick():
    A, C = G('S05'), G('S07')
    t0, t1 = A.t0, C.t1
    sc = Scene('quick', t0, {'type': 'dark', 'v': 2})
    X, Y, cw, ch, gap = 960, 550, 520, 380, 40
    sc.cam(t0, x=960, y=550, s=0.86)
    cards = [
        dict(word='先做出来', size=110, ty=0.08, sub='别等准备好', ss=44),
        dict(word='再优化', size=120, ty=0.08, sub='边做边改', ss=44),
        dict(word='持续更新', size=105, ty=0.08, sub='让方法可复用', ss=44)]
    sc.add('wall', t0 + 0.02, x=X, y=Y, cols=3, cw=cw, ch=ch, gap=gap, nodof=True, sfx='pop',
           cards=cards,
           focus=[[t0, -1], [max(t0, A.k('做出来', -0.2)), 0], [max(t0, C.k('方法', -0.2)), 2]])
    show(sc, t0, t1, **host(sc))
    KF.append(('quick', t1 - 0.3))


def end():
    E = G('END')
    sc = Scene('end', E.t0, {'type': 'end'}, sway=0)
    sc.add('endcard', E.t0, layer='screen')
    show(sc, E.t0, E.t1)
    KF.append(('end', E.t0 + 1.2))


title(); who(); cost(); income(); quick(); end()
