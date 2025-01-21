let date_js = new Date();
let current_year = date_js.getFullYear();
let current_month = date_js.getMonth() + 1;
const days = {"ja" : ['月', '火', '水', '木', '金', '土', '日'], "en" : ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']};
let first_day = 0; // 0->月曜
const isToday = "id=\"today\""

changeMonth(0) // 初期化

// Fetch API を使った参照月の切り替え関数
function changeMonth(move) {
    const url = `/create_calendar?move=${move}&month=${current_month}&year=${current_year}`; // URLに移動先と、今現在の月をクエリとして追加
    // Fetch APIでリクエストを送信
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("HTTPエラー! ステータスコード: " + response.status);
            }
            return response.json(); // JSON形式のレスポンスを解析
        })
        .then(data => {
            // データをHTMLに反映
            current_year = data.year;
            current_month = data.month;
            document.querySelector("#title_year").innerText = current_year;
            document.querySelector("#title_month").innerText = current_month;
            document.querySelector("thead").innerHTML = createCalendarHead();
            document.querySelector("tbody").innerHTML = createCalendarBody(data.calendar, data.schedules);
            
            //予定のクリック：編集画面に移動
            var events=document.querySelectorAll(".event");
            events.forEach(function(targets){
                targets.addEventListener("click",()=>{
                    window.location.href = '/edit/'+targets.textContent;
                });
            });

        })
        .catch(error => {
            // エラー時の処理
            console.error("エラーが発生しました:", error);
        });
}

function createCalendarHead() {
    calendar_head_html = ""
    days["en"].forEach(day => {
        calendar_head_html += `<th scope=\"col\">${day}</th>`;
    });

    return calendar_head_html;
}


function createCalendarBody(calendar, schedules) {
    calendar_body_html = ""
    calendar.forEach(week => {
        calendar_body_html += `<tr>`;

        week.forEach(date => {
            // 今日かどうか
            const isToday = date == date_js.getDate() ? " id=\"today\"" : "";
            // 今月かどうか
            date = date == 0 ?  "" : date;
            
            calendar_body_html +=  `<td${isToday}>
                                        <div class="top">
                                            <div class="date">${date}</div>
                                            <button type="button" class="add"><a href=/add/${current_year * 10000 + current_month * 100 + date}>+</a></button>
                                        </div>
                                        <div class="schedules">`;
            // 予定の取得
            const result = schedules.filter(schedule => schedule.add_day == date);
            console.log(schedules);
            
            result.forEach(event => {
                calendar_body_html += `<button class="event" data-id="${event.id}">${event.add_title}</button>`;
            });
            

            calendar_body_html +=  `    </div>
                                    </td>`;
        });

        calendar_body_html += `</tr>`;
    });
    
    
    return calendar_body_html;
}