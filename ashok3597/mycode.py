import boto3
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

def list_snapshots(project):
    "List of Volume snapshots"
    snapshots= []

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
	
	return

@cli.group('volumes')

def volumes():
	"""Commands for Volumes"""

@volumes.command('list')
@click.option('--project', default = None, help = "Only Volumes for the project (tag Project:<name>)")

def list_volumes(project):
    "List of EC2 Volumes"
    volumes= []

    instances = filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			print(",".join((
				v.id
				i.id
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
    instances = []

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
    instances = []

    instances = filter_instances(project)

    for i in instances:
        print("stopping [{0}..." .format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default = None, help = "Only instances for the project")

def stop_instances(project):
    """start Instances"""
    instances = []

    instances = filter_instances(project)

    for i in instances:
        print("Starting [{0}..." .format(i.id))
        i.start()

    return

if __name__="__main__":
    cli()
