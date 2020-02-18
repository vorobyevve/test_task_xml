<xsl:transform version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:my="http://tempuri.org/config"
  exclude-result-prefixes="my"
>
  <xsl:output method="xml" encoding="UTF-8" indent="yes" />
  <xsl:strip-space elements="*" />

  <my:config>
    <nameMap from="Shipments" to="shipments" />
    <nameMap from="Shipment" to="shipment" />
    <nameMap from="Container" to="-" />
  </my:config>
  <xsl:variable name="nameMap" select="document('')/*/my:config/nameMap" />

  <xsl:template match="node() | @*" name="identity">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" />
    </xsl:copy>
  </xsl:template>

  <xsl:template match="/">
    <getShipmentStatusResponse>
      <xsl:apply-templates select="@* | node()" />
    </getShipmentStatusResponse>
  </xsl:template>

  <xsl:template match="GetShipmentUpdatesResult">
    <getShipmentStatusResult>
      <outcome>
        <result>Success</result>
        <error></error>
      </outcome>
      <xsl:apply-templates select="@* | node()" />
    </getShipmentStatusResult>
  </xsl:template>

  <xsl:template match="*">
    <xsl:variable name="map" select="$nameMap[@from = name(current())]" />
    <xsl:choose>
      <xsl:when test="$map/@to = '-'">
        <xsl:apply-templates select="@* | node()" />
      </xsl:when>
      <xsl:when test="$map/@to != ''">
        <xsl:element name="{$map/@to}">
          <xsl:apply-templates select="@* | node()" />
        </xsl:element>
      </xsl:when>
      <xsl:when test="$map/@to = ''" />
      <xsl:otherwise>
        <xsl:call-template name="identity" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:transform>