$('#video-table').bootstrapTable({
    url: "search_video",
    method: "GET",
    striped: true,                      //是否显示行间隔色
    cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    toolbar: "#video-table-toolbar",

    sortable: true,                     //是否启用排序
    sortOrder: "asc",                   //排序方式
    // 分页
    sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
    pagination: true,                   //是否显示分页（*）
    pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
    pageSize: 15,                        //每页的记录行数（*）
    pageList: [15, 25, 50, 100],         //可供选择的每页的行数（*）
    search: false,                      //是否显示表格搜索
    strictSearch: true,
    showColumns: true,                  //是否显示所有的列（选择显示的列）
    showRefresh: true,                  //是否显示刷新按钮
    minimumCountColumns: 2,             //最少允许的列数
    clickToSelect: true,                //是否启用点击选中行
    //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
    uniqueId: "vid",                     //每一行的唯一标识，一般为主键列
    showToggle: true,                   //是否显示详细视图和列表视图的切换按钮
    cardView: false,                    //是否显示详细视图
    detailView: false,                  //是否显示父子表
    paginationShowPageGo:true,
    queryParams: function (params) {
        return {
            title: $("#video-query").val().trim(),
            page_size: params.limit,
            page_num: (params.offset / params.limit) + 1,
        }
    },
    responseHandler: function(res) {
        // console.log(res);
        //data["Customer_name"] = list[0].customer.name;
        return {
            "total": res.data.total,//总页数
            "rows": res.data.list   //数据
        };
    },
    columns: [{checkbox: true},
        {
            field: 'vid',
            title: '视频ID'
        },
        {
            field: 'filename',
            title: '视频名称',
            sortable: false,
        },
        {
            field: 'up_date',
            title: '上传日期',
            sortable: false,
            formatter: function (value, row, index) {
                return new Date(value).format("yyyy-MM-dd hh:mm");
            }
        },
        {
            field: 'status',
            title: '状态',
            sortable: false,
            formatter: function (value, row, index) {
                let t = "";
                if (value === "等待转码"){
                    t = "default";
                }
                else if (value === "转码中"){
                    t = "info";
                }
                else if (value === "完成"){
                    t = "success";
                }
                else if (value === "转码失败"){
                    t = "danger";
                }
                return '<span class="label label-' + t + '" >' + value +'</span>'
            }
        },
        {
            field: 'video_lst',
            title: '视频列表',
            sortable: false,
            formatter: function (value, row, index) {
                let res = [];
                let label_type = ["default", "primary", "success", "info", "warning", "danger"];
                for(let i =0;i<value.length;i++){
                    let clarity = value[i].clarity;
                    let content = clarity + "p" + "(" + value[i].width + "x" + value[i].height + ")";
                    let url = "/get_video?vid=" + row.vid + "&clarity=" + clarity;
                    let t = label_type[i % label_type.length];
                    res.push('<a target="_blank" href="' + url + '"><span class="label label-' + t + '" >' + content +'</span></a>');
                }
                return res.join("")
            }
        },
        {
            field : "operate",
            title : "操作",
            align: "center",
            formatter: function (value, row, index) {
                return [
                    '<div class="btn-group " role="group">',
                    '<button type="button" class="btn btn-default btn-sm" onclick=""><span class="glyphicon glyphicon-play" aria-hidden="true"></span>播放</button>',
                    '</div>'
                ].join('');
            } ,
        }
    ]
});