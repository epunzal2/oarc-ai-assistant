# Slurm REST API

Slurm provides a [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer) daemon
named slurmrestd. This daemon is designed to allow clients to communicate with Slurm via a REST API
(in addition to the command line interface (CLI) or C API).

Please see [OpenAPI Plugin Release Notes](openapi_release_notes.md) for changes between release
versions.

To view the currently generated API reference: [Slurm REST API Reference](rest_api.md)

## Prerequisites

slurmrestd requires additional libraries for compilation:

- [HTTP Parser](download.md#httpparser) (\>= v2.6.0)
- [LibYAML](download.md#yaml) (optional, \>= v0.2.5)
- [JSON-C](download.md#json) (\>= v1.12.0)
- [JWT Authentication](download.md#jwt) (optional)

## Stateless

Slurmrestd is stateless as it does not cache or save any state between requests. Each request is
handled in a thread and then all of that state is discarded. Any request to slurmrestd is completely
synchronous with the Slurm controller (slurmctld or slurmdbd) and is only considered complete once
the HTTP response code has been sent to the client. Slurmrestd will hold a client connection open
while processing a request. Slurm database commands are committed at the end of every request, on
the success of all API calls in the request.

Sites are strongly encouraged to setup a caching proxy between slurmrestd and clients to avoid
having clients repeatedly call queries, causing usage to be higher than needed (and causing lock
contention) on the controller.

## Run modes

Slurmrestd currently supports two run modes: inet service mode and listening mode.

### Inet Service Mode

The Slurmrestd daemon acts as an [Inet Service](https://en.wikipedia.org/wiki/Inetd) treating STDIN
and STDOUT as the client. This mode allows clients to use inetd, xinetd, or systemd socket activated
services and avoid the need to run a daemon on the host at all times. This mode creates an instance
for each client and does not support reusing the same instance for different clients.

### Listening Mode

The Slurmrestd daemon acts as a full UNIX service and continuously listens for new TCP connections.
Each connection and request are independently authenticated.

## Configuration

slurmrestd can be configured either by environment variables or command line arguments. Please see
the **doc/man/man1/slurmrestd.8** man page for details.

## OpenAPI Specification (OAS)

Slurmrestd is compliant with [OpenAPI
3.0.2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md) . The OAS can be
viewed at the following URLs:

- /openapi.json
- /openapi.yaml
- /openapi/v3

The OAS is designed to be the primary documentation for the request methods. There are several third
party tools that automatically generate documentation against the OAS output listed by
[openapi.tools.](https://openapi.tools/)

**NOTE**: Slurm attempts to strictly comply with the relevant [OpenAPI
standards](https://github.com/OAI/OpenAPI-Specification). For reasons of compatibility, Slurm may be
tested against publicly available OpenAPI client generators, but Slurm does not directly support any
of them as they are outside the control of SchedMD and may change at anytime. The goal is to comply
with the standards, supporting as many clients as possible, without favoring any one client. Sites
are always welcome to write their own clients that are OpenAPI compliant. As a rule, SchedMD will
debug the HTTP sent to and received by slurmrestd but will not directly debug any client source
code.

Tested compatibility by OpenAPI plugins:

- openapi/v0.0.37:
  - [v4.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
  - [v5.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi/v0.0.38:
  - [v4.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
  - [v5.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi/v0.0.39:
  - [v6.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi/dbv0.0.37:
  - [v4.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
  - [v5.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi/dbv0.0.38:
  - [v4.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
  - [v5.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)
- openapi/dbv0.0.39:
  - [v6.x of OpenAPI-generator](https://github.com/OpenAPITools/openapi-generator)

## Plugins

As of Slurm 20.11, the REST API uses plugins for authentication and generating content. As of
Slurm-21.08, the OpenAPI plugins are available outside of slurmrestd daemon and other slurm commands
may provide or accept the latest version of the OpenAPI formatted output. This functionality is
provided on a per command basis. These plugins can be optionally listed or selected via command line
arguments as described in the [slurmrestd](slurmrestd.md) documentation.

### Plugin life cycle

Plugins provided upstream with Slurm in any release are considered supported by that release. In
general, only the latest versioned plugins will receive minor bug fixes but all will receive
security fixes. Due to the nature of the plugins, one plugin can be supported across multiple Slurm
releases to ensure (limited) backward client compatibility. SchedMD is currently only explicitly
deprecating plugins per the [OpenAPI standard method of setting "Deprecated:
True"](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md?plain=1#L861) in the
method path. Any plugin that is not marked as deprecated will continue to exist in the next Slurm
Major release pending any critical issues which will be announced separately. Any plugin marked for
deprecation will be removed on the next Slurm major release. In general, the last three plugins have
been retained in each Slurm major release with the oldest getting marked as deprecated.

Sites are **always** encouraged to use the latest stable plugin version available for code
development. There is **no** guarantee of compatibility between different versions of the same
plugin with clients. Clients should always make sure to validate their code when migrating to newer
versions of plugins. Plugin versions will always be included in the path for every method provided
by a given plugin to ensure no two plugins will provide the same path.

As the plugins utilize the Slurm API internally, plugins that existed in previous versions of Slurm
should continue to be able to communicate with the two previous versions of Slurm, similar to other
components of Slurm. Newer plugins may have required RPC changes which will exclude them from
working with previous Slurm versions. For instance, the openapi/dbv0.0.36 plugin will not be able to
communicate with any slurmdbd servers prior to the slurm-20.11 release.

As with all other plugins in Slurm, sites are more than welcome to write their own plugins and are
suggested to submit them as code contributions via [bugzilla](https://bugs.schedmd.com/), tagged as
a contribution. The plugin API provided may change between releases which could cause site specific
plugins to break.

## Security

The Slurm REST API is written to provide the necessary functionality for clients to control Slurm
using REST commands. It is **not** designed to be directly internet facing. Only unencrypted and
uncompressed HTTP communications are supported. Slurmrestd also has no protection against man in the
middle or replay attacks. Slurmrestd should only be placed in a trusted network that will
communicate with a trusted client.

Any site wishing to expose Slurm REST API to the internet or outside of the cluster should at the
very least use a proxy to wrap all communications with TLS v1.3 (or later). You should also add
monitoring to reject any client who repeatedly attempts invalid logins at either the network
perimeter firewall or at the TLS proxy. Any client filtering that can be done via a proxy is
suggested to avoid common internet crawlers from talking to slurmrestd and wasting system resource
or even causing higher latency for valid clients. Sites are recommended to use shorter lived JWT
tokens for clients and renew often, possibly via non-Slurm JWT generator to avoid having to enforce
JWT lifespan limits. It is also suggested that sites use an authenticating proxy to handle all
client authentication against the sites preferred Single Sign On (SSO) provider instead of Slurm
**scontrol** generated tokens. This will prevent any unauthenticated client from connecting to
slurmrestd.

The Slurm REST API is an HTTP server and all general possible precautions for security of any web
server should be applied. As these precautions are site specific, it is highly recommended that you
work with your site's security group to ensure all policies are enforced at the proxy before
connecting to slurmrestd.

Slurm tries not to give potential attackers any hints when there are authentication failures. This
results in the client getting this rather terse message: `Authentication failure`. When this
happens, take a look at the logs for the relevant Slurm daemon (i.e. *slurmdbd*, *slurmctld* or
*slurmd*) for information about the actual issue.

## JSON Web Token (JWT) Authentication

slurmrestd supports using [JWT to authenticate users](jwt.md). JWT can be used to authenticate user
over REST protocol.

- User Name Header: X-SLURM-USER-NAME
- JWT Header: X-SLURM-USER-TOKEN

SlurmUser or root can provide alternative user names to act as a proxy for the given user. While
using JWT authentication, slurmrestd should be run as a unique, **unprivileged** user and group.
Slurmrestd should be provided an invalid SLURM_JWT environment variable at startup to activate JWT
authentication. This will allow users to provide their own JWT tokens while authenticating to the
proxy and ensuring against any possible accidental authorizations.

When using JWT, it is important that <u>AuthAltTypes=auth/jwt</u> be configured in your slurm.conf
for slurmrestd.

## Local Authentication

slurmrestd supports using UNIX domain sockets to have the kernel authenticate local users. By
default, slurmrestd will not start as root or SlurmUser or if the user's primary group belongs to
root or SlurmUser. Slurmrestd must be located in the Munge security domain in order to function and
communicate with Slurm in local authentication mode.

## Authenticating Proxy

There is a wide array of authentication systems that a site could choose from, if using [JWT
authentication](#jwt) doesn't meet your requirements. An authenticating proxy is setup with a JWT
token assigned to the SlurmUser that can then be used to proxy for any user on the cluster. This
ability is only allowed for SlurmUser and the root users, all other tokens will only work with their
locally assigned users.

If using a third-party authenticating proxy, it is expected that it will provide the correct HTTP
headers (**X-SLURM-USER-NAME** and **X-SLURM-USER-TOKEN**) to slurmrestd along with the user's
request.

Slurm places no requirements on the authenticating proxy beyond its being HTTP 1.1 compliant and
that it provides the correct HTTP headers to allow client authentication. Slurm will explicitly
trust the HTTP headers provided and has no way to verify them (beyond the proxy's trusted token
**X-SLURM-USER-TOKEN**). Any authenticating proxy will need to follow your site's security policies
and ensure that the proxied requests come from the correct user. These requirements are standard to
any authenticated proxy and are not Slurm specific.

A working trivial example can be found in an [internal
tool](https://gitlab.com/SchedMD/training/docker-scale-out/-/tree/master/proxy) used for testing and
training. It uses [PHP](https://www.php.net/) and [NGINX](https://www.nginx.com/) to provide the
authentication logic.

----------------------------------------------------------------------------------------------------

Last modified 16 March 2023
