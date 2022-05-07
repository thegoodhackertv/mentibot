<html>
	<title>Mentibot</title>
	<head>
		    <meta charset="UTF-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    	<link rel="stylesheet" href="style.css">
		<script language="JavaScript">
		    function showInput() {
		        document.getElementById('show_url').innerHTML = 
		                    document.getElementById("url").value;
		        document.getElementById('show_score').innerHTML = 
		                    document.getElementById("score").value;
    		}
  		</script>
	</head>
	<body>
		<!-- iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe -->
	<main>
		<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
		
		<div>
			<label for="url">URL:</label>
			<input type="text" name="url" id="url" placeholder="url" required="" >
		</div>

		<div>
			<label for="url">Score:</label>
			<input type="text" name="score" id="score" placeholder="score" required="" >
		</div>

		<div>
			<label for="url">Rounds:</label>
			<input type="text" name="rounds" id="rounds" placeholder="rounds" required="" >
		</div>
		
		<div>
		<button type="submit" name="submit" value="RUN" onclick="showInput();" >RUN</button>
		</div>

		<!-- <p><span id='show_url'></span></p>
		<p><span id='show_score'></span></p> -->
		</form>
		</main>
	</body>
		<?php
	if (isset($_POST["submit"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
	 	$url = $_POST['url'];
	 	$score = $_POST['score'];
	 	$rounds = $_POST['rounds'];
		#echo "<pre> Sending $score $rounds times to $url </pre><br>";
		$final_cmd = "python3 ../mentibot.py -u $url -s $score -r $rounds --no-banner &";
		$output = shell_exec($final_cmd);
		echo "<pre>$output</pre>";
	}
	?>	
</html> 
