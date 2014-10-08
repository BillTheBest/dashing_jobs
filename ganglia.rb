require 'httparty'
require 'addressable/uri'

# cpu_user url
uri_cpu = Addressable::URI.escape "http://localhost/ganglia/graph.php?r=hour&title=&vl=&x=&n=&hreg[]=compute&mreg[]=cpu_user&gtype=stack&glegend=hide&aggregate=1&embed=1&_=1410463742829&json=1"

# bytes_in url
uri_bytesin = Addressable::URI.escape "http://localhost/ganglia/graph.php?r=hour&title=&vl=&x=&n=&hreg[]=compute&mreg[]=bytes_in&gtype=stack&glegend=hide&aggregate=1&embed=1&_=1410794605258&json=1"

# bytes_out url
uri_bytesout = Addressable::URI.escape "http://localhost/ganglia/graph.php?r=hour&title=&vl=&x=&n=&hreg[]=compute&mreg[]=bytes_out&gtype=stack&glegend=hide&aggregate=1&embed=1&_=1410794844911&json=1"

# cpu_num url
uri_cpunum = Addressable::URI.escape "http://localhost/ganglia/graph.php?r=hour&title=&vl=&x=&n=&hreg[]=compute&mreg[]=cpu_num&gtype=stack&glegend=hide&aggregate=1&embed=1&_=1410463742829&json=1"

SCHEDULER.every '15s', :first_in => 0 do |job|
  #cpu user percentage
  total = 0.0
  node_count = 0
  response = HTTParty.get(uri_cpu)
  response.each do |host|
    data = host["datapoints"][-3][0]
    if data == "NaN"
      data = 0
    end
    total += data
    node_count += 1
  end
  average = total / node_count
  average = average.round(2)
  send_event('ganglia_cpu', { value: average })

  #bytes in
  mbitotal = 0.0
  response = HTTParty.get(uri_bytesin)
  response.each do |host|
    data = host["datapoints"][-3][0]
    if data == "NaN"
      data = 0
    end
    mbitotal += data
  end
  mbitotal = mbitotal / 1024 / 1024
  mbitotal = mbitotal.round(2)
  send_event('ganglia_bytesin', { value: mbitotal })

  #bytes in
  mbototal = 0.0
  response = HTTParty.get(uri_bytesout)
  response.each do |host|
    data = host["datapoints"][-3][0]
    if data == "NaN"
      data = 0
    end
    mbototal += data
  end
  mbototal = mbototal / 1024 / 1024
  mbototal = mbototal.round(2)
  send_event('ganglia_bytesout', { value: mbototal })
  
  # throughput, bytes total
  mbps = mbitotal + mbototal
  mbps = mbps.round(2)
  send_event('ganglia_throughput', { value: mbps})
  
  #cpu num
  total = 0
  response = HTTParty.get(uri_cpunum)
  response.each do |host|
    data = host["datapoints"][-3][0]
    if data == "NaN"
      data = 0
    end
    total += data
  end
  send_event('ganglia_cpunum', { value: total })
end