import zeroconf


def main():
    zconf = zeroconf.Zeroconf(interfaces=zeroconf.InterfaceChoice.Default)
    print("\n".join(zeroconf.ZeroconfServiceTypes.find(zc=zconf)))
    zconf.close()


if __name__ == "__main__":
    main()