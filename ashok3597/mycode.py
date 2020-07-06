import boto3
import botocore
import click

session = boto3.Session(profile_name="ashok3597")
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters = filters)

    else:
        instances = ec2.instances.all()

    return instances

@click.group()

def cli():
	"""Managing the snapshots"""
	
@snapshots.command('list')
@click.option('--project', default = None, help = "Only Snapshots for the project (tag Project:<name>)")

@click.option('--all','list_all', default = False, is_flag=True, help = "List all snapshot for all volume, not just the most recent'

def list_snapshots(project,list_all):
    "List of Volume snapshots"
    

    instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(",".join((
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime("%c")
				)))

				if s.state = 'completed' and not list_all: break 
	return

@cli.group('volumes')

def volumes():
	"""Commands for Volumes"""

@volumes.command('list')
@click.option('--project', default = None, help = "Only Volumes for the project (tag Project:<name>)")

def list_volumes(project):
    "List of EC2 Volumes"
    
    instances = filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			print(",".join((
				v.id,
				i.id,
				v.state,
				str.(v.size) + "GiB"
				v.encrypted and "Encrytped" or "Not encrypted"
			)))
	return

@cli.group('instances)
def instances():
    """commands for instances"""

@instances.command('list')
@click.option('--project', default = None, help = "Only instances for the project (tag Project:<name>)")

def list_function(project):
    "List of EC2 instances"
   
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']:t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

    return

@instances.command('stop')
@click.option('--project', default = None, help = "Only instances for the project")

def stop_instances(project):
    """Stop Instances"""

    instances = filter_instances(project)

    for i in instances:
        print("stopping [{0}..." .format(i.id))
        try:
		i.stop()
	except botocore.exceptions.ClientError as e:
		print("Could not stop {0}. ".format(i.id) + str(e))
		Continue
	   
    return

@instances.command('start')
@click.option('--project', default = None, help = "Only instances for the project")

def start_instances(project):
    """start Instances"""
    
    instances = filter_instances(project)

    for i in instances:
        print("Starting [{0}..." .format(i.id))
        try:
		i.start()
	except botocore.exceptions.ClientError as e:
		print("Could not start {0}. ".format(i.id) + str(e))
		Continue

    return
	   
@instances.command('snapshot')
@click.option('--project', default = None, help = "Only Volume for the project")

def start_snapshots(project):
    """start Snapshots"""

    instances = filter_instances(project)

    for i in instances:
	print("Stopping {0}".format(i.id))
	i.stop()
	i.wait_until_stopped()
	
	for v in i.volumes.all():
		print("Creating Snapshots of {0}".format(v.id))
		v.create_snapshot("Description = "Created by Snapshot Analyzer")
        
	print("Starting [{0}..." .format(i.id))
        
	i.start()
	i.wait_until_running()
	
	
    print('Job is done')
    return

if __name__="__main__":
    cli()
