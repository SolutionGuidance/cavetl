# Credentialing and Verification: Extract, Translate, and Load

**CAV ETL** is an [open source](LICENSE.md) standalone microservice
module meant to support access to third-party data sources useful for
credentialing and vetting health care providers.  Each microservice,
seeks to answer a specific question about a person's eligibility to
provide healthcare services.

CAV ETL consults a variety of external data sources, organizes the
information gathered from them (the "ETL" stands for "Extract,
Transform, Load"), and offers a clean API to ask about certifications,
exclusions, etc.

It was originally developed as part of the
[Provider Screening Module (PSM)](https://github.com/SolutionGuidance/psm/) 
project, and was
[separated out](https://github.com/SolutionGuidance/psm/commit/e11e2d174812e62246bf00b9f1ae7901563a902f) 
in order to serve other MMIS modules besides the PSM.

CAV ETL is not limited to provider information.  It can be used for
other credentialing needs in government health care: any effort to vet
persons or organizations in the health care industry will involve
consulting external data from multiple sources (federal, state,

regional, local).  CAV ETL offers a central place for that data to be
gathered and consulted, instead of each effort solving that problem
independently and thus duplicatively.  We believe the CAVETL stack has
applications in State MMIS systems, to health care providers screening
employees, and to health insurers vetting in-network providers.  If
you see ways to build on CAVETL, please get in touch with james AT
solutionguidance.com.  We'd love to help!

CAV ETL's goals are to:

* Lower development costs.
* Lower operational costs (including fees) for accessing the data.
* Streamline the bureaucratic process of authentication and authorization.

If you're interested in participating in CAV ETL development, or even
if you just want to discuss something with the developers, please see
the [contribution guidelines](CONTRIBUTING.md).

## Status

CAV ETL is a **work-in-progress** and is **not yet ready for
production deployment**.  Please see [INSTALL.md](INSTALL.md) for
details.

Currently supported sources:

* [List of Excluded Individuals and Entites (LEIE)](leie)
* [Social Security's Death Master File (DMF)](dmf)
 
And we have plans for many more, including certifications and PECOS,
as its new access methods develop.
