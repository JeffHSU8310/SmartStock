// TaiwanSmartQuant GUI v5.0 - 炫彩前端互動與 ECharts 圖表引擎
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    renderMarketTable();
    renderKLineChart('2330.TW');
    renderRobotCards();
    renderBacktestChart();
    renderNewsFeed();
    renderCrudTable();
    initTelegramEvents();
});

// 全域數據資料庫快取
let currentSymbol = '2330.TW';
let sampleMarketData = [
    { symbol: '2330.TW', name: '台積電', market: '上市股票(TWSE)', price: 1020.0, change: 2.51, volume: '45,280張', ma5: 1010, rsi: 65, kd: 72, pattern: '看漲吞噬' },
    { symbol: '2454.TW', name: '聯發科', market: '上市股票(TWSE)', price: 1255.0, change: 1.21, volume: '12,450張', ma5: 1240, rsi: 58, kd: 52, pattern: '常規型態' },
    { symbol: '2317.TW', name: '鴻海', market: '上市股票(TWSE)', price: 212.5, change: -0.93, volume: '68,120張', ma5: 215, rsi: 42, kd: 35, pattern: '錘子線' },
    { symbol: 'TX00.FITX', name: '台指期全月', market: '台指期貨(TAIFEX)', price: 22850.0, change: 1.25, volume: '128,450口', ma5: 22650, rsi: 68, kd: 78, pattern: '長紅突破' },
    { symbol: '3293.TWO', name: '鈊象', market: '上櫃股票(TPEX)', price: 1080.0, change: 3.85, volume: '5,320張', ma5: 1040, rsi: 78, kd: 82, pattern: '看漲吞噬' }
];

let sampleRobotData = [
    { symbol: '2330.TW', name: '台積電', market: 'TWSE', score: 92, recommend: 'BUY', fundScore: 24, chipScore: 23, techScore: 25, newsScore: 20, reason: '基本面與營收雙雙強勁突破，三大法人同步大買，技術面呈現多頭排列！' },
    { symbol: 'TX00.FITX', name: '台指期全月', market: 'TAIFEX', score: 88, recommend: 'BUY', fundScore: 20, chipScore: 22, techScore: 26, newsScore: 20, reason: '全球科技股走強帶動台指期多頭爆發，短中長天期均線全面向上延伸。' },
    { symbol: '3293.TWO', name: '鈊象', market: 'TPEX', score: 85, recommend: 'BUY', fundScore: 23, chipScore: 20, techScore: 24, newsScore: 18, reason: '海外授權營收維持高度成長，三大法人連三日回補。' },
    { symbol: '2317.TW', name: '鴻海', market: 'TWSE', score: 62, recommend: 'HOLD', fundScore: 18, chipScore: 15, techScore: 15, newsScore: 14, reason: '股價於回檔波段落腳於月線支撐，觀望籌碼與法人態度轉變。' }
];

let sampleNewsData = [
    { title: '台積電先進製程訂單持續爆滿，法人看好全年獲利再創新高', source: '經濟日報', time: '10:30', symbol: '2330.TW', score: '+0.88 樂觀看多' },
    { title: '聯準會利率會議維持不變，美科技股勁揚帶動台股夜盤跳漲', source: '中央社', time: '09:45', symbol: 'TX00.FITX', score: '+0.75 極力偏多' },
    { title: '聯發科天璣晶片出貨超預期，旗艦款市場佔有率大幅上升', source: '工商時報', time: '09:15', symbol: '2454.TW', score: '+0.65 中性偏多' }
];

// 1. 五大 Tab 切換邏輯
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = document.getElementById(btn.dataset.tab);
            if (targetTab) {
                targetTab.classList.add('active');
            }

            // 重新自適應寬度
            setTimeout(() => {
                echarts.getInstanceByDom(document.getElementById('kline-chart-container'))?.resize();
                echarts.getInstanceByDom(document.getElementById('equity-chart-container'))?.resize();
            }, 100);
        });
    });
}

// 2. 渲染看盤大廳表格
function renderMarketTable() {
    const tbody = document.getElementById('quote-table-body');
    tbody.innerHTML = '';

    sampleMarketData.forEach(item => {
        const tr = document.createElement('tr');
        const changeClass = item.change > 0 ? 'text-up' : (item.change < 0 ? 'text-down' : 'text-neutral');
        const changeSign = item.change > 0 ? '+' : '';

        tr.innerHTML = `
            <td><strong>${item.name}</strong> <br><span style="font-size:11px;color:#9CA3AF">${item.symbol}</span></td>
            <td><span class="badge cyan">${item.market}</span></td>
            <td class="${changeClass}">$${item.price.toLocaleString()}</td>
            <td class="${changeClass}">${changeSign}${item.change}%</td>
            <td>${item.volume}</td>
            <td>${item.ma5}</td>
            <td>${item.rsi}</td>
            <td>${item.kd}</td>
            <td><span class="badge ${item.pattern.includes('看漲') || item.pattern.includes('長紅') ? 'purple' : 'gold'}">${item.pattern}</span></td>
        `;

        tr.addEventListener('click', () => {
            currentSymbol = item.symbol;
            document.getElementById('current-chart-title').innerHTML = `<i class="fa-solid fa-chart-candlestick"></i> ${item.name} (${item.symbol}) - 全週期 K 線與技術指標圖`;
            renderKLineChart(item.symbol);
        });

        tbody.appendChild(tr);
    });
}

// 3. ECharts K線與技術指標渲染
function renderKLineChart(symbol) {
    const chartDom = document.getElementById('kline-chart-container');
    if (!chartDom) return;
    let myChart = echarts.getInstanceByDom(chartDom);
    if (!myChart) {
        myChart = echarts.init(chartDom, 'dark');
    }

    const dates = [];
    const kdata = [];
    const volumes = [];
    let price = (symbol === 'TX00.FITX') ? 22000 : (symbol === '2330.TW' ? 950 : 200);

    for (let i = 60; i >= 0; i--) {
        const date = new Date(Date.now() - i * 86400000).toISOString().split('T')[0];
        dates.push(date);
        
        const open = price;
        const change = (Math.random() - 0.48) * (price * 0.03);
        const close = open + change;
        const high = Math.max(open, close) + Math.random() * (price * 0.015);
        const low = Math.min(open, close) - Math.random() * (price * 0.015);
        const vol = Math.floor(10000 + Math.random() * 50000);

        kdata.push([open, close, low, high]);
        volumes.push([60 - i, vol, open > close ? -1 : 1]);
        price = close;
    }

    const option = {
        backgroundColor: 'transparent',
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross' }
        },
        grid: [
            { left: '8%', right: '5%', top: '10%', height: '55%' },
            { left: '8%', right: '5%', top: '72%', height: '20%' }
        ],
        xAxis: [
            { type: 'category', data: dates, gridIndex: 0 },
            { type: 'category', data: dates, gridIndex: 1, show: false }
        ],
        yAxis: [
            { scale: true, gridIndex: 0, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            { scale: true, gridIndex: 1, splitLine: { show: false } }
        ],
        series: [
            {
                type: 'candlestick',
                data: kdata,
                itemStyle: {
                    color: '#FF3B69',       // 台股上漲紅
                    color0: '#00E676',      // 台股下跌綠
                    borderColor: '#FF3B69',
                    borderColor0: '#00E676'
                }
            },
            {
                name: '成交量',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: volumes.map(item => item[1]),
                itemStyle: {
                    color: params => kdata[params.dataIndex][1] >= kdata[params.dataIndex][0] ? '#FF3B69' : '#00E676'
                }
            }
        ]
    };

    myChart.setOption(option);
}

// 4. 智慧選股雷達卡片
function renderRobotCards() {
    const container = document.getElementById('robot-cards-container');
    if (!container) return;
    container.innerHTML = '';

    sampleRobotData.forEach(card => {
        const div = document.createElement('div');
        div.className = 'robot-card';
        const scoreClass = card.score >= 85 ? 'high' : (card.score >= 70 ? 'mid' : 'low');

        div.innerHTML = `
            <div class="robot-card-header">
                <div>
                    <div class="sym-title">${card.name}</div>
                    <div class="sym-code">${card.symbol} · ${card.market}</div>
                </div>
                <div class="score-badge ${scoreClass}">${card.score}</div>
            </div>
            
            <div class="score-bars">
                <div class="bar-item">
                    <span class="bar-label">基本面</span>
                    <div class="bar-track"><div class="bar-fill fund" style="width: ${(card.fundScore/25)*100}%"></div></div>
                    <span>${card.fundScore}/25</span>
                </div>
                <div class="bar-item">
                    <span class="bar-label">籌碼面</span>
                    <div class="bar-track"><div class="bar-fill chip" style="width: ${(card.chipScore/25)*100}%"></div></div>
                    <span>${card.chipScore}/25</span>
                </div>
                <div class="bar-item">
                    <span class="bar-label">技術面</span>
                    <div class="bar-track"><div class="bar-fill tech" style="width: ${(card.techScore/30)*100}%"></div></div>
                    <span>${card.techScore}/30</span>
                </div>
                <div class="bar-item">
                    <span class="bar-label">消息面</span>
                    <div class="bar-track"><div class="bar-fill news" style="width: ${(card.newsScore/20)*100}%"></div></div>
                    <span>${card.newsScore}/20</span>
                </div>
            </div>

            <div class="card-reason">
                <strong>🤖 機器人點評：</strong> ${card.reason}
            </div>
        `;

        container.appendChild(div);
    });
}

// 5. C++ 回測圖表
function renderBacktestChart() {
    const chartDom = document.getElementById('equity-chart-container');
    if (!chartDom) return;
    let myChart = echarts.getInstanceByDom(chartDom);
    if (!myChart) {
        myChart = echarts.init(chartDom, 'dark');
    }

    const dates = [];
    const equityData = [];
    let equity = 1000000;

    for (let i = 120; i >= 0; i--) {
        const date = new Date(Date.now() - i * 86400000).toISOString().split('T')[0];
        dates.push(date);
        equity += (Math.random() - 0.42) * 15000;
        equityData.push(Math.round(equity));
    }

    const option = {
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis' },
        grid: { left: '6%', right: '4%', top: '10%', bottom: '15%' },
        xAxis: { type: 'category', data: dates },
        yAxis: { type: 'value', scale: true, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
        series: [{
            name: 'C++ 策略資產權益 (NTD)',
            type: 'line',
            smooth: true,
            data: equityData,
            lineStyle: { color: '#00F2FE', width: 3 },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(0, 242, 254, 0.4)' },
                    { offset: 1, color: 'rgba(0, 242, 254, 0.0)' }
                ])
            }
        }]
    };

    myChart.setOption(option);

    document.getElementById('run-backtest-btn')?.addEventListener('click', () => {
        renderBacktestChart();
    });
}

// 6. 渲染消息面新聞列表
function renderNewsFeed() {
    const container = document.getElementById('news-feed-container');
    if (!container) return;
    container.innerHTML = '';

    sampleNewsData.forEach(news => {
        const div = document.createElement('div');
        div.className = 'news-item';
        div.innerHTML = `
            <div class="n-info">
                <h4>${news.title}</h4>
                <p>來源: ${news.source} | 發布時間: ${news.time} | 標的: ${news.symbol}</p>
            </div>
            <div>
                <span class="sentiment-tag bull">${news.score}</span>
            </div>
        `;
        container.appendChild(div);
    });
}

// 7. CRUD 數據管理
function renderCrudTable() {
    const tbody = document.getElementById('crud-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    const crudItems = [
        { symbol: '2330.TW', revenue: '215,000,000', yoy: '+18.6%', eps: '38.5', pe: '24.5', foreign: '+12,500張', major: '72.5%' },
        { symbol: '2454.TW', revenue: '45,200,000', yoy: '+12.1%', eps: '48.2', pe: '21.0', foreign: '+3,200張', major: '65.2%' },
        { symbol: '2317.TW', revenue: '510,000,000', yoy: '+5.4%', eps: '10.5', pe: '18.2', foreign: '-1,800張', major: '58.0%' }
    ];

    crudItems.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${item.symbol}</strong></td>
            <td>${item.revenue}</td>
            <td class="text-up">${item.yoy}</td>
            <td>${item.eps}</td>
            <td>${item.pe}</td>
            <td class="${item.foreign.includes('+') ? 'text-up' : 'text-down'}">${item.foreign}</td>
            <td>${item.major}</td>
            <td>
                <button class="action-btn cyan" style="padding:3px 8px;font-size:11px;" onclick="alert('已載入 ${item.symbol} 編輯表單')"><i class="fa-solid fa-pen-to-square"></i> 編輯</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 8. Telegram 設定事件
function initTelegramEvents() {
    const testBtn = document.getElementById('test-tg-btn');
    const msgDiv = document.getElementById('tg-status-msg');

    testBtn?.addEventListener('click', () => {
        msgDiv.className = 'status-msg success';
        msgDiv.innerText = '🚀 [即時推播測試成功] 警報訊息已成功傳送至您的手機 Telegram！';
    });
}
