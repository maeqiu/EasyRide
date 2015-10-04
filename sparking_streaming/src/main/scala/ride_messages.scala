import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._
import org.elasticsearch.spark._
import org.json4s._
import org.json4s.jackson.JsonMethods._
import org.json4s.JsonDSL._
import org.apache.log4j.Logger
import org.apache.log4j.Level
import com.datastax.spark.connector._
import com.datastax.spark.connector.streaming._
import com.datastax.driver.core.utils._

object StreamProject {
  def main(args: Array[String]) {

    val sparkConf = new SparkConf().setAppName("stream_project")
    sparkConf.set("es.index.auto.create", "true")
  	sparkConf.set("es.nodes", "ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200") 
  	sparkConf.set("spark.executor.memory", "5g")
  	sparkConf.set("spark.streaming.receiver.maxRate", "3800")
    
    
    val sc = new SparkContext(sparkConf)
    val ssc = new StreamingContext(sc, Seconds(2))
	val sqlContext = new SQLContext(sc)
	
	val zkQuorum = "ec2-52-8-225-175.us-west-1.compute.amazonaws.com:2181"
    val group = "myGroup"
    val topic = Map("RideRequests" -> 1)
    val kafkaStream = KafkaUtils.createStream(ssc, zkQuorum, group, topic).map(_._2)
	
	def single_to_double(digit: String): String = if (digit.length==1) "0"+digit else digit
	
    val parsed_message = kafkaStream.map( x => parse(x) )

    val messages_all = parsed_message.map( message => {val date_array = compact(message \ "timestamp").tail.dropRight(1).split(",")
    						    (compact(render( message \ "userID" )).toInt,							     
							    compact(render( message \ "messageID" )).toInt,
							    compact(render( message \ "phone" )).tail.dropRight(1), 
							    (date_array(0) + single_to_double(date_array(1)) + single_to_double(date_array(2))).toInt,
							    (single_to_double(date_array(3)) + single_to_double(date_array(4)) + single_to_double(date_array(5))).toInt,
							     compact(render( message \ "latdep" )).toDouble,
							     compact(render( message \ "longdep" )).toDouble,
							     compact(render( message \ "latarr" )).toDouble,
							     compact(render( message \ "longarr" )).toDouble,
							     compact(render( message \ "drFlag" )).toInt )}
					       )
					       				       
	val output = messages_all.map(x => Map("userid"-> x._1,
	"messageid"->x._2, "phone"->x._3, "date"->x._4, "time"->x._5,
	"deplocation"-> Map("lat"->x._6, "lon"->x._7),
	"arrlocation"-> Map("lat"->x._8, "lon"->x._9),
	"drflag"->x._10))
					       				       
	messages_all.print				       				       
		
	output.print
	
	output.foreachRDD { rdd =>
    	rdd.saveToEs("messages/myMessages")
    }
  	  	
    // Start the computation
    ssc.start()  
    ssc.awaitTermination()
  }
}

