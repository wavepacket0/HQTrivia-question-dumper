<h1><p align="center">HQTrivia Question Dumper</p></h1>

This is a Python 3.0+ (tested on 3.6) script to dump all the HQTrivia questions available on HQBuff. It is based on their API used to dynamically build HQBuff pages when you browse them.

This is the general API layout:
<img src="./controllers_brief.svg" height="70%">
Example to fetch the game held on 2018-09-01, country code us:

    https://hqbuff.com/api/us/2018-09-01


Script features:

 - Default worker threads : cpu count * 2
 - Uses 5 worker threads if cpu count is None
 - Multiple parallel requests using concurrent.futures.ThreadPoolExecutor
 - Takes 18 seconds to dump the whole us game questions on Ununtu vm with 2 cores
