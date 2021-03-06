import os

from awscli.clidriver import create_clidriver

def aws_cli(*cmd):
    old_env = dict(os.environ)
    try:

        # Environment
        env = os.environ.copy()
        env['LC_CTYPE'] = u'en_US.UTF'
        env['AWS_ACCESS_KEY_ID'] = env['S3_ACCESS_KEY']
        env['AWS_SECRET_ACCESS_KEY'] = env['S3_SECRET_KEY']
        os.environ.update(env)

        # Run awscli in the same process
        exit_code = create_clidriver().main(*cmd)

        # Deal with problems
        if exit_code > 0:
            raise RuntimeError('AWS CLI exited with code {}'.format(exit_code))
    finally:
        os.environ.clear()
        os.environ.update(old_env)

def download(bucket, src, dest):
    aws_cli(['s3', 'sync', 's3://{}'.format(os.path.normpath("{}/{}").format(bucket, src)), dest, '--delete'])