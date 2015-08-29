keyup_handler = function(evt) {
    if (evt.key == '+')
        next_page();
    else if (evt.key == '-')
        prev_page();

    // assume page entry
    var key = parseInt(evt.key);
    if (isNaN(key)) {
        return;
    }

    var span_pnum = $('#pagenum');
    if (span_pnum.text().length == 3) {
        if (key != 0)
            span_pnum.text(key);
        else
            return;
    } else {
        span_pnum.text(span_pnum.text() + key);
    }

    if (span_pnum.text().length == 3) {
        post_nav(parseInt(span_pnum.text()));   
    }
};

next_page = function() {
    var current_page = parseInt($('#pagenum').text());
    if (current_page == 999)
        return;
    post_nav(current_page + 1);
}

prev_page = function() {
    var current_page = parseInt($('#pagenum').text());
    if (current_page == 100)
        return;
    post_nav(current_page - 1);
}

post_nav = function(pagenum) {
    $.ajax({
        type: 'POST',
        url: $('#navigation_url').text(),
        data: JSON.stringify({page: pagenum}),
        success: function(data) { 
            $('#pagenum').text(pagenum);
            render_data(data); 
            get_excerpt(pagenum);
        },
        error: function(data) { console.log(data); },
        contentType: "application/json",
        dataType: 'html'
    });
}

get_excerpt = function(pagenum) {
    console.log('getting excerpt')
    $.ajax({
        type: 'POST',
        url: $('#excerpt_url').text(),
        data: JSON.stringify({page: pagenum}),
        success: function(data) {
            render_excerpt(data);
        },
        error: function(data) { console.log(data); },
        contentType: "application/json",
        dataType: 'json'
    });
}

render_data = function(data) {
    $('#post_data_placeholder').html(data);
}

render_excerpt = function(data) {
    $('#excerpt').text(data.excerpt);
}

// digital clock code

days = [
    'Sön', 'Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör'
];

months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'
];


digital_clock = function() {
    var datetime = new Date();
    
    var h = datetime.getHours();
    var m = datetime.getMinutes();
    var s = datetime.getSeconds();
    
    var day = datetime.getDay();
    var date = datetime.getDate();
    var month = datetime.getMonth();

    $('#cdayname').text(days[day]);
    $('#cdaynum').text(prepend_zero(date));
    $('#cmonth').text(months[month]);

    $('#chour').text(prepend_zero(h));
    $('#cminute').text(prepend_zero(m));
    $('#csecond').text(prepend_zero(s));

    setTimeout('digital_clock()', 1000);
};

prepend_zero = function(num) {
    if (num < 10)
        return '0' + num;
    return num;
}

$(window).load(function() {
    digital_clock();

    $(this).keyup(keyup_handler);
});
