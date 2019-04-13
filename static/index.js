$(function () {
    var bsTable = $('#mytable').bootstrapTable({
      method: 'get',
      contentType: 'application/x-www-form-urlencoded',
      url: '/data',
      height: tableHeight(),
      locale: 'zh-CN',
      dataField: "res",
      sidePagination: 'server',
      pageSize:10,//单页记录数
      pageList:[10,20,30],//分页步进值
      //showRefresh:true,//刷新按钮,
      pageNumber: 1, //初始化加载第一页，默认第一页
      pagination:true,//是否分页
      queryParamsType: 'limit',
      queryParams:queryParams,//请求服务器时所传的参数
      columns: [
        {
          title: 'id',
          field: 'p_id',
          align: 'center',
          sortable: true,
        }, {
          title: 'zol_id',
          field: 'zol_id',
          align: 'center',
        }, {
          title: '图片',
          field: 'image_url',
          align: 'center',
          formatter: format_image_url,
        }, {
          title: '名称',
          field: 'p_name',
          align: 'center'
        }, {
          title: '价格',
          field: 'price',
          align: 'center',
          sortable: true,
          formatter: format_price,
        }, {
          title: 'CPU',
          field: 'p_cpu',
          align: 'center'
        }, {
          title: '前摄像头',
          field: 'front_camera',
          align: 'center'
        }, {
          title: '后摄像头',
          field: 'rear_camera',
          align: 'center'
        }, {
          title: '内存',
          field: 'ram',
          align: 'center',
          sortable: true,
          formatter: format_ram,
        }, {
          title: '电池',
          field: 'battery',
          align: 'center'
        }, {
          title: '屏幕大小',
          field: 'screen',
          align: 'center'
        }, {
          title: '分辨率',
          field: 'screen',
          align: 'center'
        }, {
          title: '详情',
          field: 'web_url',
          align: 'center',
          formatter: format_web_url,
        },
      ]
    });
    //tableHeight函数
    function tableHeight(){
        //可以根据自己页面情况进行调整
        return $(window).height() -100;
    }
    
    function format_image_url(value, row, index, field) {
      return '<img src="'+value+'">'
    }

    function format_web_url(value, row, index, field) {
      return '<a href="'+value+'" target="_blank"><button type="button" class="btn btn-primary">详情</button></a>'
    }

    function format_ram(value, row, index, field) {
        return value + 'GB'
    }

    function format_price(value, row, index, field) {
        if (value === -1 || value === '-1') {
            return '价格待定'
        }
    }

    //请求服务数据时所传参数
    function queryParams(params){
        return{
            limit: params.limit,
            offset: params.offset,
            sort: params.sort,
            order: params.order,
            name:$('#phone_name_input').val(),
        }
    }

    $('#find_button').on('click', function (e) {
      $('#mytable').bootstrapTable('refreshOptions',{pageNumber:1,pageSize:10});//便可以了
      $('#mytable').bootstrapTable('refresh', {url: '/data'});
    });

    $('#find_data_from').on('submit', function (e) {
      e.preventDefault();
      $('#mytable').bootstrapTable('refreshOptions',{pageNumber:1,pageSize:10});//便可以了
      $('#mytable').bootstrapTable('refresh', {url: '/data'});
    })
});
