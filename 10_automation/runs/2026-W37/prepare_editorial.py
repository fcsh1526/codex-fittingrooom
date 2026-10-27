import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
raw = list(csv.DictReader((RUN / 'source_perplexity.csv').open(encoding='utf-8-sig')))
assert len(raw) == 20 and {r['week'] for r in raw} == {'2026-W37'}

# Each entry: name, outfit, palette, fabric, fit, decision, proof, scene, action.
looks = [
('霧灰薄襯衫配奶油白洋裝','霧灰無內裡棉質薄襯衫；奶油白不透膚細肩帶小腿中長洋裝；白色低筒帆布鞋；深海軍藍小肩包；細銀耳環','霧灰／奶油白／海軍藍','輕薄棉府綢／不透膚棉混紡／帆布','襯衫下襬及上臀、敞開；洋裝自然直落；平底鞋','冷氣房用可脫薄襯衫罩住肩臂，洋裝本身可以單穿','敞開襯衫露出完整洋裝，薄袖折痕與肩包帶清楚可見','有大片側窗的社區圖書館入口閱讀區，木書架與石磨地板','站在還書桌旁把一本無字素封面書放到桌上'),
('霧藍薄襯衫配深藍洋裝','霧藍無內裡亞麻混紡薄襯衫；深海軍藍方領寬肩帶中長洋裝；米白帆布便鞋；灰色帆布小托特包；銀色耳釘','霧藍／海軍藍／米白','亞麻混紡／薄棉質／帆布','襯衫寬鬆及上臀；洋裝自然A字及小腿；鞋子平底','以可脫襯衫調節室內外溫差，避免外套與內搭都厚重','寬肩帶洋裝可獨立成套，薄襯衫捲袖和敞開前襟顯示輕量層次','採光明亮的花藝工作坊，入口木桌放著素色花瓶','一手拿起桌上一枝白色桔梗，另一手自然垂下'),
('白色短夾克配靛藍寬褲','光學白無鋪棉短版薄斜紋夾克；淡藍短袖棉襯衫紮入腰頭；深靛藍高腰薄料長寬褲；黑色平底樂福鞋；焦糖棕小方包','白／淡藍／深靛藍／焦糖棕','薄棉斜紋／棉府綢／垂墜萊賽爾','夾克下襬停腰骨；長褲離地且露出鞋尖','上身用腰骨長度的短外套，讓寬褲腰線與垂墜清楚可見','白夾克下襬與高腰深藍褲形成清楚長短差，褲管不堆地','小型建築事務所的開放式樣品桌旁，側窗日光','把一片材質樣板平放在桌角'),
('沙色短外套配霧灰寬褲','沙色腰骨長度薄棉短夾克；白色圓領短袖上衣紮入腰頭；霧灰高腰薄料長寬褲；深棕低跟包鞋；黑色小肩包','沙色／白／霧灰／深棕','薄棉斜紋／棉針織／薄混紡西裝料','夾克方形短版；褲身長直垂墜且不拖地','寬褲配短外套時讓腰頭露出，避免上下兩件都蓋住腰線','沙色短下襬、白色內搭與灰褲腰頭的邊界清楚','陶藝展館的明亮入口展廊，石質展台與開放門廊','一手輕推開展廊的木門'),
('海軍藍肩線外套配緞面裙','深海軍藍無內裡肩線清楚的輕薄外套；米白圓領無袖緞面中長洋裝；黑色低跟樂福鞋；黑色小腋下包；細銀耳環','海軍藍／米白／黑','薄西裝料／不透膚緞面／霧面皮革','外套及上臀、自然肩線不誇張；裙身直落小腿','只用肩線明確的外套增加結構，洋裝保留柔軟垂墜','深色肩線與米白緞面柔軟折光形成對比','室內小型室內樂演出場地的側窗休息廳','將一張素色無字節目冊放在窄桌上'),
('挺版無袖上衣配垂墜長裙','米白無袖立領棉府綢上衣；墨藍高腰緞面中長直裙；黑色低跟尖方頭鞋；黑色小肩包；銀色耳釘','米白／墨藍／黑','挺薄棉府綢／不透膚緞面／霧面皮革','上衣立領離頸、下襬紮入；裙身直落小腿','天熱時把結構放在薄上衣的立領，其餘用柔軟裙身平衡','米白立領有明確形狀，墨藍裙身自然垂墜而不蓬起','設計書店的白牆展示桌區，大片玻璃窗側光','一手輕翻展示桌上的無字圖像書'),
('白襯衫配酒紅T字帶鞋','白色短袖棉府綢襯衫；深灰高腰及踝直筒褲；酒紅色低粗跟T字帶鞋，腳背中央直帶連接踝前橫帶、包頭；黑色小肩包；黑色窄皮帶','白／深灰／酒紅／黑','棉府綢／薄西裝料／霧面皮革','直筒褲止於踝上、不遮腳背；鞋跟低而寬','基本款配T字帶鞋時縮短褲長，露出腳背的T字結構','白襯衫與灰褲保持簡潔，酒紅鞋的直帶與橫帶完整可見','城市街角烘焙店的開放式騎樓，上午側光','站在窗口前把一個無字紙袋接到手中'),
('黑色中長裙配奶油白T字帶鞋','黑色短袖棉質上衣；黑色高腰中長A字裙；奶油白方頭低粗跟T字帶鞋，腳背直帶連接橫帶；黑色小肩包；細銀耳釘','黑／奶油白／銀','棉質針織／薄棉斜紋／霧面皮革','裙長到小腿中段；鞋面完全露出；上衣紮入','中長裙用單色簡潔剪裁，讓淺色T字帶鞋清楚呈現','黑裙下露出奶油白鞋面與T字交叉結構，不加其他復古裝飾','街區小型畫廊的半戶外石階平台，柔和午後光','平穩走向敞開的畫廊門口'),
('奶油白棉麻配焦糖麂皮包','奶油白無袖棉麻襯衫；深咖啡高腰薄棉麻直筒褲；焦糖色短毛麂皮小肩包；黑色低跟樂福鞋；細銀耳環','奶油白／深咖啡／焦糖／黑','棉麻／短毛麂皮／霧面皮革','上衣紮入；直筒褲離地；小包位於腰側','入秋先用麂皮小包，衣服保留薄棉麻','焦糖麂皮絨面貼近奶油白棉麻，黑鞋低調不搶材質對比','社區咖啡店外有遮蔭的長木椅旁','一手扶著椅背準備坐下，肩包自然垂在腰側'),
('淺藍襯衫裙配巧克力麂皮包','淺藍短袖棉質襯衫中長洋裝，配同布腰帶；巧克力棕短毛麂皮小肩包；黑色平底包鞋；銀色耳釘','淺藍／巧克力棕／黑','薄棉府綢／短毛麂皮／霧面皮革','裙身自然A字至小腿；腰帶鬆繫；袖口不緊','薄襯衫裙搭一個深棕麂皮包，以小面積換材質','淺藍棉質裙身與深棕絨面包在腰側相鄰，厚材質只用在小包','河岸附近的獨立雜貨店門廊，明亮漫射日光','一手提起桌上的素色陶杯查看杯形'),
]

rows=[]
for i, v in enumerate(looks):
    name,outfit,palette,fabric,fit,decision,proof,scene,action=v
    rows.append(dict(carousel_id=f'2026-W37-{i//2+1:03}',look_order=i%2+1,look_name=name,
        opening_hook=decision,dressing_decision=decision,occasion=['冷氣房閱讀／花藝課','上班／看展','藝文活動／書店','通勤／畫廊','咖啡廳／週末採買'][i//2],
        clothing_item=outfit,color_palette=palette,fabric=fabric,fit=fit,styling_rules=decision,
        visual_proof=proof,practical_rule=decision,scene=scene,visible_action=action,
        frame_plan='carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16',required_frames=3,status='editorial_approved'))

def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)

write(ROOT/'03_research/editorial_look_plans/2026-W37.csv',rows)
approved=[]
problems=['室外偏熱、冷氣房又需要遮住肩臂，如何選可脫的薄層？','寬鬆上衣和寬褲一起穿，如何讓腰線清楚？','想穿柔軟衣料，如何保留一處明確的衣服輪廓？','基本款想搭T字帶鞋，褲裙要多長才看得見鞋帶？','想加麂皮材質，又不想整身厚重，配件如何選？']
for i in range(5):
    r=raw[i*4].copy(); first=rows[i*2]
    r.update(id=f'W37-E{i+1:03}',status='editorial_approved',clothing_item=first['clothing_item'],color_palette=first['color_palette'],fabric=first['fabric'],fit=first['fit'],styling_rules=first['styling_rules'])
    r['notes']='; '.join(f'{k}={v}' for k,v in dict(editorial_status='approved',audience_problem=problems[i],editorial_answer=first['dressing_decision'],opening_hook=first['opening_hook'],visual_proof=first['visual_proof'],practical_rule=first['practical_rule'],source_url='https://mika-lin-weekly.pplx.app/weeks/2026-W37.html',source_prompt_id=raw[i*4]['id']).items())
    approved.append(r)
write(ROOT/'03_research/editorial_overrides/2026-W37.csv',approved)
print('Prepared 5 editorial rows and 10 complete looks.')
