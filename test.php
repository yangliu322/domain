<?php
	$redis = new Redis();
	$redis->connect('127.0.0.1',6379);
	if(empty($_POST["domain"])==false){
		
		$domain = $_POST["domain"];
		
		$crawl = $_POST["crawl"];
		$translator = $_POST["translator"];
		$label = $_POST["label"];
	
		$redis->select(0);//选择数据库
		$redis->set($domain,$domain);

		$redis->select(4);//选择数据库
		$redis->set($domain,$domain);
		
		
		
	}else if(empty($_POST["domains"])==false)
	{
		$domains = $_POST["domains"];
		$group = explode("\n",$domains);
		foreach($group as $domain){
			$redis->select(0);//选择数据库
			$redis->set($domain,$domain);

			$redis->select(4);//选择数据库
			$redis->set($domain,$domain);
		}
		
	}else if(!empty($_FILES['file']['tmp_name']))
	{
		$fileName = $_FILES["file"]["name"];
		$tmp_name =  $_FILES["file"]["tmp_name"] ;
		move_uploaded_file($tmp_name,"file/".$fileName);
		$file = fopen("file/".$fileName, "r") or exit("Unable to open file!");
		/*while(!feof($file))
		{
			$dm = fgets($file);
			$dm = str_replace('\r\n', '', $dm);
			$redis->select(0);//选择数据库
			$redis->set($dm,$dm);

			$redis->select(4);//选择数据库
			$redis->set($dm,$dm);
		}*/
		$file_path = "file/".$fileName;
		if(file_exists($file_path)){
			$str = file_get_contents($file_path);//将整个文件内容读入到一个字符串中

			$str = str_replace("\r\n","<br />",$str);
			$group = explode("<br />",$str);
			foreach($group as $domain){
				$redis->select(0);//选择数据库
				$redis->set($domain,$domain);

				$redis->select(4);//选择数据库
				$redis->set($domain,$domain);
			}
		}
		fclose($file);
	}else{
		$redis->select(4);//选择数据库
		$keys = $redis->keys("*");
		foreach($keys as $key){
			$arr[$key]["schedule"] = 25;
			$arr[$key]["key"] = $key;
			$arr[$key]["english"] ="";
			$arr[$key]["chinese"] ="";
			$arr[$key]["label"] = "";
		}
		
		$redis->select(1);//选择数据库
		$keys = $redis->keys("*");
		foreach($keys as $key){
			$arr[$key]["english"] = $redis->get($key);
			$arr[$key]["schedule"] = 50;
		}
		
		
		$redis->select(2);//选择数据库
		$keys = $redis->keys("*");
		foreach($keys as $key){
			$arr[$key]["chinese"] = $redis->get($key);
			$arr[$key]["schedule"] = 75;
		}
		
		
		$redis->select(3);//选择数据库
		$keys = $redis->keys("*");
		foreach($keys as $key){
			$arr[$key]["label"] = $redis->get($key);
			$arr[$key]["schedule"] = 100;
		}
		//var_dump($arr);
		echo json_encode( $arr);
	}
?>