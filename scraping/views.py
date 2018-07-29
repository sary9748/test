from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.utils.html import mark_safe

# Create your views here.
def appmain(request):
	Prefectures = {'宗谷地方':'301.html','上川・留萌地方':'302.html','網走・北見・紋別地方':'303.html','釧路・根室・十勝地方':'304.html','胆振・日高地方':'305.html','石狩・空知・後志地方':'306.html','渡島・檜山地方':'307.html','青森県':'308.html','岩手県':'310.html',
	'宮城県':'312.html','秋田県':'309.html','山形県':'311.html','福島県':'313.html','茨城県':'314.html','栃木県':'316.html','群馬県':'315.html','埼玉県':'317.html','千葉県':'318.html','東京都':'319.html','神奈川県':'320.html','新潟県':'323.html',
	'富山県':'324.html','石川県':'325.html','福井県':'326.html','山梨県':'321.html','長野県':'322.html','岐阜県':'328.html','静岡県':'327.html','愛知県':'329.html','三重県':'330.html','滋賀県':'334.html','京都府':'333.html','大阪府':'331.html',
	'兵庫県':'332.html','奈良県':'335.html','和歌山県':'336.html','鳥取県':'339.html','島根県':'337.html','岡山県':'340.html','広島県':'338.html','山口県':'345.html','徳島県':'343.html','香川県':'341.html','愛媛県':'342.html','高知県':'344.html',
	'福岡県':'346.html','佐賀県':'347.html','長崎県':'348.html','熊本県':'349.html','大分県':'350.html','宮崎県':'351.html','鹿児島県':'352.html','沖縄本島地方':'353.html','大東島地方':'354.html','宮古島地方':'355.html','八重島地方':'356.html'}
	try:
		URL = 'https://www.jma.go.jp/jp/yoho/' + Prefectures[request.GET.get('pref_name')]#頭文字を選んだURL
	except:
		return render(request, 'scraping/tenki.html', {})

	res = requests.get(URL) #URLから情報を取得
	try:
		res.raise_for_status() #エラー処理
	except:
		return render(request, 'scraping/tenki.html', {})
	response = BeautifulSoup(res.content, "html.parser") #htmlを取得
	for img in response.find_all("img"):
		img["src"] = "../static/"+str(img["src"])
	table_infos = str(response.select('#forecasttablefont')[0]) #tdタグの単語を取得。
	old_html = table_infos.split('\n')
	new_html = [str('<td class="titleText">\n<h1>'+request.GET.get('pref_name')+'</h1>\n</td>\n')]
	for delete in old_html:
		if '<input' not in delete:
			new_html.append(delete)
	new_html.append('<div class="fortemplete">(/:のち, |:時々または一時)</div>')
	pref_dic = {
		'pref_name':request.GET.get('pref_name'),
		'weather':mark_safe('\n'.join(new_html))
	}

	return render(request, 'scraping/tenki.html', pref_dic)
