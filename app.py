from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response

    data = request.json
    query = data.get('query', '')
    stock = data.get('stock', '')

    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    message = client.messages.create(
        model='claude-opus-4-5',
        max_tokens=1000,
        system="""당신은 한국 주식 전문 애널리스트입니다. 종목 질문에 전문적으로 답변하세요.
[수급 동향] [기술적 분석] [밸류에이션] [투자 의견] 4개 섹션으로 구분해서 300~400자로 답변하세요.""",
        messages=[{'role': 'user', 'content': f'종목: {stock}\n질문: {query}'}]
    )

    response = jsonify({'result': message.content[0].text})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
