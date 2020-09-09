<?php
if(is_array($_GET)&&count($_GET)>0)//先判断是否通过get传值了
{
    if(isset($_GET["name"]))//是否存在"id"的参数
	{
        $name = $_GET["name"];
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>Spica Admin</title>
<link rel="stylesheet" href="css/materialdesignicons.min.css">
<link rel="stylesheet" href="css/style.css">
<script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
		  
</head>
	<body>
	<div class="container-scroller d-flex">
		<div class="container-fluid page-body-wrapper">
			<nav class="navbar col-lg-12 col-12 px-0 py-0 py-lg-4 d-flex flex-row">
			<div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
			  <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
				<span class="mdi mdi-menu"></span>
			  </button>
			  <div class="navbar-brand-wrapper">
				<a class="navbar-brand brand-logo" href="index.html"><img src="images/logo.svg" alt="logo"/></a>
			  </div>
			  <h4 class="font-weight-bold mb-0 d-none d-md-block mt-1">Welcome back, <?php echo $name;?></h4>
			  <ul class="navbar-nav navbar-nav-right">
				<li class="nav-item">
				  <h4 id="time" class="mb-0 font-weight-bold d-none d-xl-block">Mar 12, 2019 - Apr 10, 2019</h4>
				</li>
				<li class="nav-item dropdown mr-1">
				  <a class="nav-link count-indicator dropdown-toggle d-flex justify-content-center align-items-center" id="messageDropdown" href="#" data-toggle="dropdown">
					<i class="mdi mdi-calendar mx-0"></i>
					<span class="count bg-info">2</span>
				  </a>
				</li>
				<li class="nav-item dropdown mr-2">
				  <a class="nav-link count-indicator dropdown-toggle d-flex align-items-center justify-content-center" id="notificationDropdown" href="#" data-toggle="dropdown">
					<i class="mdi mdi-email-open mx-0"></i>
					<span class="count bg-danger">1</span>
				  </a>
				</li>
			  </ul>
			  <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
				<span class="mdi mdi-menu"></span>
			  </button>
			</div>
			<div class="navbar-menu-wrapper navbar-search-wrapper d-none d-lg-flex align-items-center">
			  <ul class="navbar-nav mr-lg-2">
				<li class="nav-item nav-search d-none d-lg-block">
				  <div class="input-group">
					<input type="text" class="form-control" placeholder="Search Here..." aria-label="search" aria-describedby="search">
				  </div>
				</li>
			  </ul>  
			</div>
		  </nav>
			<div class="main-panel">
				<div class="content-wrapper">
				  <div class="row">
					<div class="col-12">
					  <div class="card">
						<div class="card-body">
						  <h4 class="card-title">Domain Name Analysis System</h4>
						  <div class="forms-sample">
							 <div class="form-group">
							  <label for="exampleInputName1">Single domain name</label>
							  <input type="text" id="domain" class="form-control" id="exampleInputName1" placeholder="domain">
							</div>
							<div class="form-group">
							  <label for="exampleTextarea1">Multiple domain names</label>
							  <textarea class="form-control" name="domains" id="domains" rows="4"></textarea>
							</div>
							<div class="form-group">
							  <label>File upload</label>
							  <input type="file" name="file" class="file-upload-default" id="upload">
							  <div class="input-group col-xs-12">
								<input type="text" class="form-control file-upload-info" disabled placeholder="Upload File">
								<span class="input-group-append">
								  <button class="file-upload-browse btn btn-primary" type="button">Upload</button>
								</span>
							  </div>
							</div>
							<div class="form-inline">
								<div style="width:33.3%;float:left" >
									<label for="exampleSelectGender">Crawling API</label>
									<select class="form-control" name="crawl" id="crawl" style="width:100%">
										<option value="bing">Bing crawl</option>
										<option value="baidu">Baidu crawl</option>
									</select>
								</div>
								<div style="width:33.3%" >
									<label for="exampleSelectGender">Translation API</label>
									<select class="form-control" name="translator" id="translator" style="width:100%">
										<option value="tencent">Tencent Translation</option>
										<option value="baidu">Baidu translator</option>
									</select>
								</div>
								<div style="width:33.4%;float:right" >
									<label for="exampleSelectGender">Label API</label>
									<select class="form-control" name="label" id="label" style="width:100%">
										<option value="baidu">Baidu Tagging</option>
									</select>
								</div>
							</div>
							<button id="submit" class="btn btn-primary mr-2">Submit</button>
							<button class="btn btn-light">Cancel</button>
						  </div>
						</div>
					  </div>
					</div>
					<div class="col-lg-12 grid-margin stretch-card">
					  <div class="card">
						<div class="card-body">
						  <h4 class="card-title">Process information</h4>
						  <div class="table-responsive">
							<table class="table table-striped">
							  <thead>
								<tr>
								  <th>
									domain
								  </th>
								  <th>
									English description
								  </th>
								  <th>
									Chinese description
								  </th>
								  <th>
									schedule
								  </th>
								  <th>
									label
								  </th>
								</tr>
							  </thead>
							  <tbody id="tb">
							  </tbody>
							</table>
						  </div>
						</div>
					  </div>
					</div>
				  </div>
				</div>
			  </div>
			</div>
		  </div>
		  <script src="js/file-upload.js"></script>
		  <script src="js/template.js"></script>
				<script>
					var date = new Date();
					var year = date.getFullYear(); //获取当前年份(2位)
					var month = date.getMonth(); //获取当前月份(0-11,0代表1月);
					var day = date.getDate(); //获取当前日(1-31)
					var en_mon_arr = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Spt","Oct","Nov","Dec"];
					var time = en_mon_arr[month]+" "+day+","+year;
					document.getElementById("time").innerHTML = time;
					function sub(){
						var dm = document.getElementById("domain").value;
						var dms = document.getElementById("domains").value;
						
						var formData1 = new FormData();
						var name = $("#upload").val();
						formData1.append("file",$("#upload")[0].files[0]);
						formData1.append("name",name);
						formData1.append("domain",dm);
						formData1.append("domains",dms);
						$.ajax({
							type:"POST",
							url:"test.php",
							data:formData1,
							dataType:"formData",
							processData: false,// 告诉jQuery不要去处理发送的数据(必须设置)
							contentType: false, // 告诉jQuery不要去设置Content-Type请求头（必须设置）
							success:function(data){
							//alert("数据: " + data + "\n状态: " + status);
								var json = JSON.parse(data);
								var tb = document.getElementById("tb");
								tb.innerHTML = "";
								for(var i in json)  
								{  
									var tr = document.createElement("tr");
									
									var th1 = document.createElement("td");
									var textnode1 = document.createTextNode(i);
									th1.appendChild(textnode1);
									tr.appendChild(th1);
									
									var th2 = document.createElement("td");
									var textnode2 = document.createTextNode(json[i]["english"]);
									th2.appendChild(textnode2);
									tr.appendChild(th2);
									
									var th3 = document.createElement("td");
									var textnode3 = document.createTextNode(json[i]["chinese"]);
									th3.appendChild(textnode3);
									tr.appendChild(th3);
									
									var th4 = document.createElement("td");
									var div1 = document.createElement("div");
									div1.setAttribute("class","progress");
									var div2 = document.createElement("div");
									div2.setAttribute("class","progress-bar bg-success");
									div2.setAttribute("style","width:"+json[i]["schedule"]+"%");
									//var textnode4 = document.createTextNode(json[i]["schedule"]);
									div1.appendChild(div2);
									th4.appendChild(div1);
									tr.appendChild(th4);
									
									var th5 = document.createElement("td");
									var textnode5 = document.createTextNode(json[i]["label"]);
									th5.appendChild(textnode5);
									tr.appendChild(th5);
									
									tb.appendChild(tr);
								} 
							}
						});					
					}
					sub();
					var fn = function(){
						var dm = "";
						var dms = "";
						var cl = "";
						var tsr = "";
						var lab = "";
						$.post("test.php",
							{ domain:dm, domains:dms,crawl:cl,translator:tsr,label:lab },
							function(data,status){
							//alert("数据: " + data + "\n状态: " + status);
							var json = JSON.parse(data);
							var tb = document.getElementById("tb");
							tb.innerHTML = "";
							for(var i in json)  
							{  
								var tr = document.createElement("tr");
								
								var th1 = document.createElement("td");
								var textnode1 = document.createTextNode(i);
								th1.appendChild(textnode1);
								tr.appendChild(th1);
								
								var th2 = document.createElement("td");
								var textnode2 = document.createTextNode(json[i]["english"]);
								th2.appendChild(textnode2);
								tr.appendChild(th2);
								
								var th3 = document.createElement("td");
								var textnode3 = document.createTextNode(json[i]["chinese"]);
								th3.appendChild(textnode3);
								tr.appendChild(th3);
								
								var th4 = document.createElement("td");
								var div1 = document.createElement("div");
								div1.setAttribute("class","progress");
								var div2 = document.createElement("div");
								div2.setAttribute("class","progress-bar bg-success");
								div2.setAttribute("style","width:"+json[i]["schedule"]+"%");
								//var textnode4 = document.createTextNode(json[i]["schedule"]);
								div1.appendChild(div2);
								th4.appendChild(div1);
								tr.appendChild(th4);
								
								var th5 = document.createElement("td");
								var textnode5 = document.createTextNode(json[i]["label"]);
								th5.appendChild(textnode5);
								tr.appendChild(th5);
								
								tb.appendChild(tr);
							} 
						});
						setTimeout(fn, 100);
					}
					fn();
					$("#submit").click(sub);
				</script>
		  
		</body>
</html>