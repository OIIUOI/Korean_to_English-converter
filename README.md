# Korean_to_English-converter

한글을 영타로 쳤을 때 한글로 변환한다

한영키가 되지 않아 후다닥 만들었는데 만들고 나서 찾아보니 이미 한영타 변환기가 웹상으로 있어서 조금 허탈했었다는 이야기..

[# 한/영타 변환기](https://www.theyt.net/wiki/%ED%95%9C%EC%98%81%ED%83%80%EB%B3%80%ED%99%98%EA%B8%B0)

게다가 내가 어떤 글을 썼는지 영어에서 한글로 바로 변환해서 보여주기 때문에 

파이썬에서는 한번 프로그램을 돌려야 내가 무슨 소리를 썼는지 알아볼 수 있는데 

그 웹페이지에서는 바로바로 볼 수 있기 때문에 더 쉽게 사용할 수 있었다 

그리고 비우기 버튼도 있고 복사 버튼도 있어서 아주 유용함..

약 20년간 사용된 페이지인데 나의 기술은 약 20년이 뒤쳐진 게 아닌가라는 생각이 약간 들기도 했지만 자바스크립트의 라이브적인 면모를 잘 볼 수 있지 않나 언어의 특징 때문에 그렇지 않나! 라고 위안을 삼아본다


영타에서 한글로 변하는 것은 딕셔너리를 써서 쉽게 해결할 수 있는 문제였지만 문제는 한글은 초성,중성,종성이 존재한다는 것이였다.
그래서 영어에서 한글로는 바뀌지만 ㄱ ㅏ ㄴ ㅏ 이런식으로 써진다는 문제가 있어 찾아보니
한글 유틸이라고 하는 패키지가 있어서 코드를 일부 차용하였다
그런데 이것은 "앉" "ㅢ" 같은 키보드를 2번 쳐야 나타나는 글들은 합쳐주지 못했기 때문에
모음이 두번 연속해서 나올 경우는 없기 때문에 "ㅢ"같은 부분은 바로 replace로 치환했고
"앉" "삯" 같이 받침이 2개로 이루어져 있는 경우에는 그 다음 글자가 자음이거나 더이상 글자가 없는 경우에 치환되도록 해였다
지금은 쓰고자 하는 말이 별 이상 없이 써져서 아 그래도 하루만에 후다닥 잘 했다 라는 생각!
