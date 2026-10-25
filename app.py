import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='Умка — учусь у тебя!', page_icon='🧑‍🎓', layout='wide')
DEFAULT = {
 'topic':'Как беречь природу?',
 'stages':[
  {'name':'Объясни мне','icon':'🎤','question':'Привет! Объясните мне, пожалуйста, почему важно беречь природу?','followup':'А что произойдёт, если люди перестанут заботиться о природе?','hint':'Попросите объяснить простыми словами и привести причину.'},
  {'name':'Найди мою ошибку','icon':'🔍','question':'Я думаю, что пластиковая бутылка исчезает в природе за один день. Я прав?','followup':'Ой, я ошибся! Почему пластиковые отходы опасны для окружающей среды?','hint':'Предложите детям найти ошибку и аргументировать исправление.'},
  {'name':'Приведи пример','icon':'💡','question':'Как я могу помогать природе каждый день? Назовите конкретные действия.','followup':'А какое из этих действий мы можем начать делать уже сегодня?','hint':'Попросите привести пример из школы или дома.'},
  {'name':'Экзамен для Умки','icon':'🎓','question':'Теперь вы мои учителя! Задайте мне вопрос по теме, а потом проверьте мой ответ.','followup':'Мой ответ: «Чтобы беречь природу, нужно меньше мусорить и экономить ресурсы». Оцените его и дополните!','hint':'Ученики оценивают ответ персонажа и дополняют его.'}
 ]
}

if 'scenario' not in st.session_state: st.session_state.scenario=json.loads(json.dumps(DEFAULT,ensure_ascii=False))
if 'stage' not in st.session_state: st.session_state.stage=0
if 'step' not in st.session_state: st.session_state.step=0
if 'done' not in st.session_state: st.session_state.done=[False]*4
if 'emotion' not in st.session_state: st.session_state.emotion='curious'

st.markdown('''<style>
.stApp{background:radial-gradient(ellipse at 50% 0%,#233568,#0b1128 70%);color:#f5f7ff}
.block-container{max-width:1200px;padding-top:1.5rem}
h1,h2,h3,p,label{color:#f5f7ff!important}
.hero{text-align:center;padding:12px 0 24px}.hero h1{font-size:clamp(34px,5vw,58px);margin:0}.hero p{font-size:20px;color:#cbd9ff!important}
.robot-box{background:linear-gradient(150deg,#253e79,#111e42);border:2px solid #536bc0;border-radius:30px;padding:20px 10px;text-align:center;box-shadow:0 20px 50px #0005}
.robot-box img{max-width:290px;margin:auto;animation:bob 2.7s ease-in-out infinite;filter:drop-shadow(0 12px 12px #0005)}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.bubble{background:#f8faff;color:#15214a;border-radius:24px 24px 24px 6px;padding:24px;font-size:24px;font-weight:650;min-height:160px;box-shadow:0 12px 32px #0004}
.stage{background:#1c2c58;border:1px solid #5670b8;border-radius:15px;padding:13px;text-align:center;min-height:95px}
.stage small{color:#d5e2ff}div.stButton button{border-radius:14px;min-height:52px;font-weight:700}
</style>''',unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧑‍🎓 УМКА — УЧУСЬ У ТЕБЯ!</h1><p>Сегодня ученик — учитель! • Универсальный школьный лайфхак</p></div>',unsafe_allow_html=True)
scenario=st.session_state.scenario
with st.sidebar:
 st.header('👩‍🏫 Панель учителя')
 st.caption('Все изменения сохраняются в текущей сессии браузера. Экспортируйте сценарий, чтобы не потерять его.')
 with st.expander('✏️ Редактировать сценарий'):
  scenario['topic']=st.text_input('Тема урока',scenario['topic'])
  for i,s in enumerate(scenario['stages']):
   st.markdown(f'**{i+1}. {s["name"]}**')
   s['question']=st.text_area('Первая реплика',s['question'],key=f'q{i}')
   s['followup']=st.text_area('Вторая реплика',s['followup'],key=f'f{i}')
   s['hint']=st.text_input('Подсказка учителю',s['hint'],key=f'h{i}')
  st.success('Изменения применяются автоматически.')
 st.download_button('💾 Скачать сценарий JSON',data=json.dumps(scenario,ensure_ascii=False,indent=2),file_name='umka_scenario.json',mime='application/json',use_container_width=True)
 upload=st.file_uploader('📂 Загрузить сценарий JSON',type='json')
 if upload is not None and st.button('Применить загруженный сценарий'):
  try:
   obj=json.load(upload)
   if not isinstance(obj.get('topic'),str) or len(obj.get('stages',[]))!=4 or any(not all(isinstance(s.get(k),str) for k in ('name','icon','question','followup','hint')) for s in obj['stages']):
    raise ValueError('Неверная структура файла')
   st.session_state.scenario=obj
   st.session_state.stage=0;st.session_state.step=0;st.session_state.done=[False]*4
   st.rerun()
  except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:st.error(f'Не удалось загрузить: {e}')
 if st.button('🔄 Начать урок заново',use_container_width=True):
  st.session_state.stage=0;st.session_state.step=0;st.session_state.done=[False]*4;st.session_state.emotion='curious';st.rerun()

st.markdown(f'### 📚 Тема: {scenario["topic"]}')
progress=sum(st.session_state.done)*25
st.progress(progress/100,text=f'Прогресс обучения Умки: {progress}% (этапы пройдены)')
cols=st.columns(4)
for i,(col,s) in enumerate(zip(cols,scenario['stages'])):
 with col:
  mark='✅' if st.session_state.done[i] else ('🔵' if i==st.session_state.stage else '⚪')
  st.markdown(f'<div class="stage">{mark} {s["icon"]}<br><b>{s["name"]}</b></div>',unsafe_allow_html=True)
  if st.button('Выбрать этап',key=f'choose{i}',use_container_width=True):
   st.session_state.stage=i;st.session_state.step=0;st.session_state.emotion='curious';st.rerun()

s=scenario['stages'][st.session_state.stage]
st.divider()
left,right=st.columns([1,2],gap='large')
with left:
 mood=st.session_state.emotion
 st.image(str(Path(__file__).parent / f'umka_{mood}.svg'),width=290)
 st.markdown('<div style="text-align:center"><h2>Умка</h2><p>Ваш виртуальный одноклассник</p></div>',unsafe_allow_html=True)
with right:
 st.subheader(f'{s["icon"]} {s["name"]}')
 line=s['question'] if st.session_state.step==0 else s['followup']
 st.markdown(f'<div class="bubble">{line}</div>',unsafe_allow_html=True)
 st.info(f'💡 Учителю: {s["hint"]}')
 st.caption('Умка работает по сценарию. Ответы учеников оценивает учитель, а не программа.')
 a,b,c=st.columns(3)
 with a:
  if st.button('💬 Следующая реплика',use_container_width=True):
   st.session_state.step=1;st.session_state.emotion='thinking';st.rerun()
 with b:
  if st.button('👏 Этап пройден',use_container_width=True):
   st.session_state.done[st.session_state.stage]=True
   st.session_state.emotion='happy'
   st.rerun()
 with c:
  if st.button('➡️ Следующий этап',use_container_width=True):
   st.session_state.stage=(st.session_state.stage+1)%4
   st.session_state.step=0;st.session_state.emotion='curious';st.rerun()
if all(st.session_state.done):
 st.balloons()
 st.success('🎓 Умка: «Спасибо, ребята! Теперь я лучше понимаю эту тему. Сегодня вы были моими учителями!»')
st.caption('Без ИИ и API • Данные не отправляются внешней языковой модели • Для занятий с интерактивной доской')
