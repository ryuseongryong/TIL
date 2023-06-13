package main

import (
	"net"
)

// type SignatureAlgorithm int
// type PublicKeyAlgorithm int
// type KeyUsage int
// type ExtKeyUsage int

// type Certificate struct {
// 	Raw                     []byte // Complete ASN.1 DER content (certificate, signature algorithm and signature).
// 	RawTBSCertificate       []byte // Certificate part of raw ASN.1 DER content.
// 	RawSubjectPublicKeyInfo []byte // DER encoded SubjectPublicKeyInfo.
// 	RawSubject              []byte // DER encoded Subject
// 	RawIssuer               []byte // DER encoded Issuer

// 	Signature          []byte
// 	SignatureAlgorithm SignatureAlgorithm

// 	PublicKeyAlgorithm PublicKeyAlgorithm
// 	PublicKey          any

// 	Version             int
// 	SerialNumber        *big.Int
// 	Issuer              pkix.Name
// 	Subject             pkix.Name
// 	NotBefore, NotAfter time.Time // Validity bounds.
// 	KeyUsage            KeyUsage

// 	// Extensions contains raw X.509 extensions. When parsing certificates,
// 	// this can be used to extract non-critical extensions that are not
// 	// parsed by this package. When marshaling certificates, the Extensions
// 	// field is ignored, see ExtraExtensions.
// 	Extensions []pkix.Extension

// 	// ExtraExtensions contains extensions to be copied, raw, into any
// 	// marshaled certificates. Values override any extensions that would
// 	// otherwise be produced based on the other fields. The ExtraExtensions
// 	// field is not populated when parsing certificates, see Extensions.
// 	ExtraExtensions []pkix.Extension

// 	// UnhandledCriticalExtensions contains a list of extension IDs that
// 	// were not (fully) processed when parsing. Verify will fail if this
// 	// slice is non-empty, unless verification is delegated to an OS
// 	// library which understands all the critical extensions.
// 	//
// 	// Users can access these extensions using Extensions and can remove
// 	// elements from this slice if they believe that they have been
// 	// handled.
// 	UnhandledCriticalExtensions []asn1.ObjectIdentifier

// 	ExtKeyUsage        []ExtKeyUsage           // Sequence of extended key usages.
// 	UnknownExtKeyUsage []asn1.ObjectIdentifier // Encountered extended key usages unknown to this package.

// 	// BasicConstraintsValid indicates whether IsCA, MaxPathLen,
// 	// and MaxPathLenZero are valid.
// 	BasicConstraintsValid bool
// 	IsCA                  bool

// 	// MaxPathLen and MaxPathLenZero indicate the presence and
// 	// value of the BasicConstraints' "pathLenConstraint".
// 	//
// 	// When parsing a certificate, a positive non-zero MaxPathLen
// 	// means that the field was specified, -1 means it was unset,
// 	// and MaxPathLenZero being true mean that the field was
// 	// explicitly set to zero. The case of MaxPathLen==0 with MaxPathLenZero==false
// 	// should be treated equivalent to -1 (unset).
// 	//
// 	// When generating a certificate, an unset pathLenConstraint
// 	// can be requested with either MaxPathLen == -1 or using the
// 	// zero value for both MaxPathLen and MaxPathLenZero.
// 	MaxPathLen int
// 	// MaxPathLenZero indicates that BasicConstraintsValid==true
// 	// and MaxPathLen==0 should be interpreted as an actual
// 	// maximum path length of zero. Otherwise, that combination is
// 	// interpreted as MaxPathLen not being set.
// 	MaxPathLenZero bool

// 	SubjectKeyId   []byte
// 	AuthorityKeyId []byte

// 	// RFC 5280, 4.2.2.1 (Authority Information Access)
// 	OCSPServer            []string
// 	IssuingCertificateURL []string

// 	// Subject Alternate Name values. (Note that these values may not be valid
// 	// if invalid values were contained within a parsed certificate. For
// 	// example, an element of DNSNames may not be a valid DNS domain name.)
// 	DNSNames       []string
// 	EmailAddresses []string
// 	IPAddresses    []net.IP
// 	URIs           []*url.URL

// 	// Name constraints
// 	PermittedDNSDomainsCritical bool // if true then the name constraints are marked critical.
// 	PermittedDNSDomains         []string
// 	ExcludedDNSDomains          []string
// 	PermittedIPRanges           []*net.IPNet
// 	ExcludedIPRanges            []*net.IPNet
// 	PermittedEmailAddresses     []string
// 	ExcludedEmailAddresses      []string
// 	PermittedURIDomains         []string
// 	ExcludedURIDomains          []string

// 	// CRL Distribution Points
// 	CRLDistributionPoints []string

// 	PolicyIdentifiers []asn1.ObjectIdentifier
// }

// type HostnameError struct {
// 	Certificate *Certificate
// 	Host        string
// }

// func (h HostnameError) Error() string {
// 	c := h.Certificate

// 	if !c.hasSANExtension() && matchHostnames(c.Subject.CommonName, h.Host) {
// 		return "x509: certificate relies on legacy Common Name field, use SANs instead"
// 	}

// 	var valid string
// 	if ip := net.ParseIP(h.Host); ip != nil {
// 		// Trying to validate an IP
// 		if len(c.IPAddresses) == 0 {
// 			return "x509: cannot validate certificate for " + h.Host + " because it doesn't contain any IP SANs"
// 		}
// 		for _, san := range c.IPAddresses {
// 			if len(valid) > 0 {
// 				valid += ", "
// 			}
// 			valid += san.String()
// 		}
// 	} else {
// 		valid = strings.Join(c.DNSNames, ", ")
// 	}

// 	if len(valid) == 0 {
// 		return "x509: certificate is not valid for any names, but wanted to match " + h.Host
// 	}
// 	return "x509: certificate is valid for " + valid + ", not " + h.Host
// }

func test(h string) error {
	candidateIP := h
	if len(h) >= 3 && h[0] == '[' && h[len(h)-1] == ']' {
		candidateIP = h[1 : len(h)-1]
	}
	if ip := net.ParseIP(candidateIP); ip != nil {
		// We only match IP addresses against IP SANs.
		// See RFC 6125, Appendix B.2.
		for _, candidate := range IPAddresses {
			if ip.Equal(candidate) {
				return nil
			}
		}
	}
}

func (c *Certificate) VerifyHostname(h string) error {
	candidateIP := h
	if len(h) >= 3 && h[0] == '[' && h[len(h)-1] == ']' {
		candidateIP = h[1 : len(h)-1]
	}
	if ip := net.ParseIP(candidateIP); ip != nil {
		// We only match IP addresses against IP SANs.
		// See RFC 6125, Appendix B.2.
		for _, candidate := range c.IPAddresses {
			if ip.Equal(candidate) {
				return nil
			}
		}
		return HostnameError{c, candidateIP}
	}
}



In general, HTTP/TLS requests are generated by dereferencing a URI.
As a consequence, the hostname for the server is known to the client.
If the hostname is available, the client MUST check it against the
server's identity as presented in the server's Certificate message,
in order to prevent man-in-the-middle attacks.

If the client has external information as to the expected identity of
the server, the hostname check MAY be omitted.  (For instance, a
client may be connecting to a machine whose address and hostname are
dynamic but the client knows the certificate that the server will
present.)  In such cases, it is important to narrow the scope of
acceptable certificates as much as possible in order to prevent man
in the middle attacks.  In special cases, it may be appropriate for
the client to simply ignore the server's identity, but it must be
understood that this leaves the connection open to active attack.

If a subjectAltName extension of type dNSName is present, that MUST
be used as the identity.  Otherwise, the (most specific) Common Name
field in the Subject field of the certificate MUST be used.  Although
the use of the Common Name is existing practice, it is deprecated and
Certification Authorities are encouraged to use the dNSName instead.

Matching is performed using the matching rules specified by
[PKIX-OLD].  If more than one identity of a given type is present in
the certificate (e.g., more than one dNSName name, a match in any one
of the set is considered acceptable.)  Names may contain the wildcard
character * which is considered to match any single domain name
component or component fragment.  E.g., *.a.com matches foo.a.com but
not bar.foo.a.com. f*.com matches foo.com but not bar.com.

In some cases, the URI is specified as an IP address rather than a
hostname.  In this case, the iPAddress subjectAltName must be present
in the certificate and must exactly match the IP in the URI.